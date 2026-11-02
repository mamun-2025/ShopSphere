

from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction

from carts.models import Cart, CartItem
from products.models import Product
from shipping.models import ShippingAddress, ShippingMethod
from taxes.services import get_default_tax_rate

from .models import Order, OrderItem


ZERO = Decimal("0.00")
CENT = Decimal("0.01")


def money(value):
   return Decimal(str(value)).quantize(
      CENT,
      rounding=ROUND_HALF_UP,
   )


@transaction.atomic
def create_order_from_items(
   *,
   user,
   items,
   shipping_address_id,
   shipping_method_id,
   payment_method=Order.PaymentMethod.COD,
):
   """
   Create an order from a list of product/quantity pairs.

   Example: 
      items=[
         {"product_id": 10, "quantity": 2},
      ]

   This function does not read, modify, or clear the cart.
   """


   # 1. Validate and normalize requested items.
   if not items:
      raise ValidationError(
         "There are no products to order."
      )

   quantities = {}

   for item in items:
      try:
         product_id = int(item["product_id"])
         quantity = int(item["quantity"])
      except (KeyError, TypeError,ValueError):
         raise ValidationError(
            "Invalid product or quantity."
         )

      if product_id < 1 or quantity < 1:
         raise ValidationError(
            "Product and quantity must be valid."
         )

      quantities[product_id] = (
         quantities.get(product_id, 0) + quantity
      )


   # 2. Lock products and read current database values.
   products = {
      product.pk: product
      for product in (
         Product.objects
         .select_for_update()
         .filter(pk__in=quantities.keys())
         .order_by("pk")
      )
   }

   if len(products) != len(quantities):
      raise ValidationError(
         "One or more products are no longer available."
      )


   # 3. Validate product status and stock.
   for product_id, quantity in quantities.items():
      product = products[product_id]

      if not product.is_active:
         raise ValidationError(
            f"{product.name} is no longer available."
         )

      if product.stock < quantity:
         raise ValidationError(
            f"Insufficient stock for {product.name}."
            f"Available: {product.stock}."
         )


   # 4. Lock and validate the user's shipping address.
   address = (
      ShippingAddress.objects
      .select_for_update()
      .select_related("zone")
      .filter(
         pk=shipping_address_id,
         user=user,
      ).first()
   )

   if address is None:
      raise ValidationError(
         "Please select a valid delivery address."
      )

   if address.zone is None and not address.zone.is_active:
      raise ValidationError(
         "The selected delivery zone is unavailable."
      )


   # 5. Lock and validate the shipping method.
   shipping_method = (
      ShippingMethod.objects
      .select_for_update()
      .select_related("zone")
      .filter(
         pk=shipping_method_id,
         is_active=True,
      ).first()
   )

   if shipping_method is None:
      raise ValidationError(
         "Please select an available shipping method."
      )

   if (
      shipping_method.zone_id is None
      or not shipping_method.zone.is_active
      or shipping_method.zone_id != address.zone_id
   ):
      raise ValidationError(
         "The delivery method does not match your address."
      )


   # 6. Validate the payment method.
   if payment_method != Order.PaymentMethod.COD:
      raise ValidationError(
         "Unsupported payment method."
      )


   # 7. Calculate merchandise subtotal.
   subtotal = ZERO

   for product_id, quantity in quantities.items():
      product = products[product_id]
      subtotal += money(product.price * quantity)

   subtotal = money(subtotal)


   # 8. Get configured tax rate.
   tax_rate_obj = get_default_tax_rate()

   tax_rate = (
      Decimal(str(tax_rate_obj.rate))
      if tax_rate_obj is not None
      else ZERO
   )


   # 9. Calculate tax and create item snapshots.
   item_snapshots = []
   total_tax = ZERO 

   for product_id, quantity in quantities.items():
      product = products[product_id]

      unit_price = money(product.price)
      line_total = money(unit_price * quantity)

      if product.is_taxable:
         item_tax_rate = tax_rate
         line_tax = money(
            line_total * item_tax_rate / Decimal("100")
         )
      else:
         item_tax_rate = ZERO
         line_tax = ZERO

      total_tax += line_tax

      item_snapshots.append({
         "product": product,
         "product_name": product.name,
         "unit_price": unit_price,
         "quantity": quantity,
         "is_taxable": product.is_taxable,
         "tax_rate": item_tax_rate,
         "tax_amount": line_tax,
         "line_total": line_total,
      })

   total_tax = money(total_tax)


   # 10. Calculate shipping on pre-tax merchandise subtotal.
   threshold = shipping_method.free_shipping_threshold

   if threshold is not None and subtotal >= threshold:
      shipping_fee = ZERO
   else:
      shipping_fee = money(shipping_method.cost)

   service_fee = ZERO 


   # 11. Calculate final total on the server 
   total = money(
      subtotal
      + total_tax
      + shipping_fee
      + service_fee
   )


   # 12. Create order and snapshot shipping details.
   order = Order.objects.create(
      user=user,
      payment_method=payment_method,
      status=Order.Status.PENDING,
      payment_status=Order.PaymentStatus.UNPAID,

      shipping_full_name = address.full_name,
      shipping_phone=address.phone,
      shipping_address_line=address.address_line,
      shipping_area=address.area,
      shipping_city_or_district=address.city_or_district,
      shipping_postal_code=address.postal_code,
      shipping_instructions=address.delivery_instructions,

      shipping_zone_name=address.zone.name,
      shipping_method_name=shipping_method.name,
      estimated_delivery_days=shipping_method.estimated_delivery_days,

      subtotal=subtotal,
      tax_amount=total_tax,
      shipping_fee=shipping_fee,
      service_fee=service_fee,
      total=total,
   )


   # 13. Create order item snapshots
   OrderItem.objects.bulk_create([
      OrderItem(
         order=order,
         product=snapshot["product"],
         product_name=snapshot["product_name"],
         unit_price=snapshot["unit_price"],
         quantity=snapshot["quantity"],
         is_taxable=snapshot["is_taxable"],
         tax_rate=snapshot["tax_rate"],
         tax_amount=snapshot["tax_amount"],
         line_total=snapshot["line_total"],
      )
      for snapshot in item_snapshots
   ])


   # 14. Deduct stock after all validations.
   for product_id, quantity in quantities.items():
      product = products[product_id]
      product.stock -= quantity
      product.save(update_fields=["stock"])

   return order




@transaction.atomic
def create_order_from_cart(
   *,
   user,
   shipping_address_id,
   shipping_method_id,
   payment_method=Order.PaymentMethod.COD,
):
   """
   Create an order from the user's cart.
   Clear the cart only after successful order creation.
   """

   try:
      cart = (
         Cart.objects
         .select_for_update()
         .get(user=user)
      )
   except Cart.DoesNotExist:
      raise ValidationError("Your cart does not exist.")

   cart_items = list(
      CartItem.objects
      .select_for_update()
      .filter(cart=cart)
      .order_by("pk")
   )

   if not cart_items:
      raise ValidationError("Your cart is empty.")

   order_items = [
      {
         "product_id": item.product_id,
         "quantity": item.quantity,
      }
      for item in cart_items
   ]

   order = create_order_from_items(
      user=user,
      items=order_items,
      shipping_address_id=shipping_address_id,
      shipping_method_id=shipping_method_id,
      payment_method=payment_method,
   )

   # Only Cart Checkout clears cart items.
   CartItem.objects.filter(
      cart=cart
   ).delete()

   return order 









      





   


   





   






