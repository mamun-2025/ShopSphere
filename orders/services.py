

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
   return Decimal(value).quantize(
      CENT,
      rounding=ROUND_HALF_UP,
   )


@transaction.atomic
def create_order_from_cart(
   *,
   user,
   shipping_address_id,
   shipping_method_id,
   payment_method=Order.PaymentMethod.COD,
):
   """
   Validate the current cart, create a permanent order,
   reduce stock, and clear the cart atomically.
   """

   # 1. Lock this user's cart.
   try:
      cart = (
         Cart.objects
         .select_for_update()
         .get(user=user)
      )
   except Cart.DoesNotExist:
      raise ValidationError("Your cart does not exist.")


   # 2. Lock cart items.
   cart_items = list(
      CartItem.objects
      .select_for_update()
      .filter(cart=cart)
      .order_by("pk")
   )

   if not cart_items:
      raise ValidationError("Your cart is empty.")


   # 3. Lock products and fetch their current database values.
   product_ids = [item.product_id for item in cart_items]

   products = {
      product.pk: product 
      for product in (
         Product.objects
         .select_for_update()
         .filter(pk__in=product_ids)
         .order_by("pk")
      )
   }


   # 4. Validate products and stock
   for item in cart_items:
      product = products.get(item.product_id)

      if product is None:
         raise ValidationError(
            "A product in your cart is no longer available."
         )

      if not product.is_active:
         raise ValidationError(
            f"{product.name} is no longer available."
         )

      if item.quantity < 1:
         raise ValidationError(
            f"Invalid quantity for {product.name}."
         )

      if product.stock < item.quantity:
         raise ValidationError(
            f"Insufficient stock for {product.name}. "
            f"Avilable: {product.stock}."
         )


   # 5.Validate the address belongs to this user.
   address = (
      ShippingAddress.objects
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

   if address.zone is None or not address.zone.is_active:
      raise ValidationError(
         "The select delivery zone is unavailable."
      )



   # 6.Lock and validate the shipping method.
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
         "The select delivery method does not match."
         "Your delivery address"
      )


   # 7. Validate payment method.
   if payment_method != Order.PaymentMethod.COD:
      raise ValidationError(
         "Unsupported payment method."
      )


   # 8. Calculate current subtotal and taxable subtotal.
   subtotal = ZERO

   for item in cart_items:
      product = products[item.product_id]

      line_total += money(product.price * item.quantity)
      subtotal += line_total 

   subtotal = money(subtotal)


   # 9.Get the current configured tax rate.
   tax_rate_obj = get_default_tax_rate()

   if tax_rate_obj is not None:
      tax_rate = Decimal(str(tax_rate_obj.rate))
   else:
      tax_rate = ZERO


   # 10. Calculate tax per order item.
   item_snapshots = []
   total_tax = ZERO
   taxable_subtotal = ZERO

   for item in cart_items:
      product = products[item.product_id]

      line_total = money(product.price * item.quantity)

      if product.is_taxable:
         item_tax_rate = tax_rate
         taxable_subtotal += line_total

         line_tax = money(
            line_total * item_tax_rate / Decimal("100")
         )
      else:
         item_tax_rate =  ZERO
         line_tax = ZERO

      total_tax += line_tax

      item_snapshots.append(
         {
            "product": product,
            "product_name": product.name,
            "unit_price": money(product.price),
            "quantity": item.quantity,
            "is_taxable": product.is_taxable,
            "tax_rate": item_tax_rate,
            "tax_amount": line_tax,
            "line_total": line_total,
         }
      )

   total_tax = money(total_tax)
   taxable_subtotal = money(taxable_subtotal)

   # 11.Calculate shipping on pre-tax merchandise subtotal
   threshold = shipping_method.free_shipping_threshold

   if threshold is not None and subtotal >= threshold:
      shipping_fee = ZERO
   else:
      shipping_fee = money(shipping_method.cost)

   service_fee = ZERO


   # 12. Calculate the final total on the server.
   total = money(
      subtotal
      + total_tax
      + shipping_fee
      + service_fee
   )

   # 13. Create the permanent order and address snapshot.
   order = Order.objects.create(
      user=user,
      payment_method=payment_method,
      status=Order.Status.PENDING,
      payment_status=Order.PaymentStatus.UNPAID,

      shipping_full_name=address.full_name,
      shipping_phone=address.phone,
      shipping_address_line=address.address_line,
      shipping_area=address.area,
      shipping_city_or_district=address.city_or_district,
      shipping_postal_code=address.postal_code,
      shipping_instructions=address.delivery_instructions,

      shipping_method_name=shipping_method.name,
      estimated_delivery_days=shipping_method.estimated_delivery_days,

      subtotal=subtotal,
      tax_amount=total_tax,
      shipping_fee=shipping_fee,
      service_fee=service_fee,
      total=total,
   )

   # 14. Create order item snapshots
   order_items = [
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
   ]

   OrderItem.objects.bulk_create(order_items)

   # 15. Reduce stock only after all validations pass.
   for item in cart_items:
      product = products[item.product_id]
      product.stock -= item.quantity
      product.save(update_fields=["stock"])


   # 16. Clear the cart
   CartItem.objects.filter(
      cart=cart
   ).delete()

   return order 

   






