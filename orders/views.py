
from decimal import Decimal
from types import SimpleNamespace

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from products.models import Product
from carts.models import Cart
from shipping.services import calculate_shipping_for_subtotal, get_shipping_selection
from taxes.services import calculate_items_totals

from .models import Order
from .services import create_order_from_items, create_order_from_cart


# CheckOut View
class CheckoutView(LoginRequiredMixin, View):
   template_name = "orders/checkout.html"

   def get_checkout_source(self, request):
      return request.session.get("checkout_source", "cart")

   def get_checkout_items(self, request):
      """
      Return a unified list of items for Cart or Buy Now.
      Each item has product, quantity and line_total.
      """
      source = self.get_checkout_source(request)

      if source == "cart":
         cart = Cart.objects.filter(
            user=request.user
         ).first()

         if not cart:
            raise ValidationError(
               "Your cart does not exist."
            )

         cart_items = list(
            cart.items.select_related("product").all()
         )

         if not cart_items:
            raise ValidationError("Your cart is empty.")

         stock_issues = cart.get_stock_issues()

         if stock_issues:
            messages.error(
               request,
               "Please resolve stock issues before checkout.",
            )

         items = []

         for item in cart_items:
            items.append(
               SimpleNamespace(
                  product=item.product,
                  quantity=item.quantity,
                  line_total=(
                     item.product.price * item.quantity
                  ),
               )
            )

         return items


      if source == "buy_now":
         product_id = request.session.get(
            "buy_now_product_id"
         )
         quantity = request.session.get(
            "buy_now_quantity"
         )

         try:
            product_id = int(product_id)
            quantity = int(quantity)
         except (TypeError, ValueError):
            raise ValidationError(
               "Your buy now session is invalid. Please try again."
            )

         if quantity < 1:
            raise ValidationError("Invalid product quantity.")

         product = Product.objects.filter(
            pk=product_id,
            is_active=True,
         ).first()

         if product is None:
            raise ValidationError(
               "The product is no longer available."
            )

         if product.stock < quantity:
            raise ValidationError(
               f"Insufficient stock for {product.name}."
               f"Available: {product.stock}."
            )

         return [
            SimpleNamespace(
               product=product,
               quantity=quantity,
               line_total=product.price * quantity,
            )
         ]

      raise ValidationError("Invalid checkout source.")


   def get(self, request):
      try:
         checkout_items = self.get_checkout_items(request)

      except ValidationError as exc:
         for error in exc.messages:
            messages.error(request, error)

         if self.get_checkout_source(request) == "buy_now":
            request.session.pop("checkout_source", None)
            request.session.pop("buy_now_product_id", None)
            request.session.pop("buy_now_quantity", None)

         return redirect("carts:detail")

      

      shipping_method, shipping_address = get_shipping_selection(
         request
      )

      if not shipping_method or not shipping_address:
         messages.info(
            request,
            "Choose a delivery address and shipping method first.",
         )
         return redirect(
            "shipping:options"
         )

      tax_summary = calculate_items_totals(checkout_items)
      shipping_summary = calculate_shipping_for_subtotal(
         subtotal=tax_summary["subtotal"],
         shipping_method=shipping_method,
         shipping_address=shipping_address,
      )

      if shipping_summary["shipping_method"] is None:
         messages.error(
            request,
            "Your shipping selection is no longer valid."
         )
         return redirect("shipping:options")

      service_fee = Decimal("0.00")
      shipping_fee = shipping_summary["shipping_fee"]

      total = (
         tax_summary["total"]
         + shipping_fee
         + service_fee
      )

      context = {
         "checkout_items": checkout_items,
         "checkout_source": self.get_checkout_source(request),

         "shipping_method": shipping_method,
         "shipping_address": shipping_address,

         "shipping_fee": shipping_fee,
         "free_shipping": shipping_summary["free_shipping"],

         "service_fee": service_fee,
         "total": total,

         **tax_summary,
      }

      return render(
         request,
         self.template_name,
         context,
      )


   def post(self, request):
      shipping_method_id = request.session.get(
         "shipping_method_id"
      )
      shipping_address_id = request.session.get(
         "shipping_address_id"
      )

      if not shipping_method_id or not shipping_address_id:
         messages.error(
            request,
            "Choose your delivery details before placing an order.",
         )
         return redirect(
            "shipping:options"
         )

      source = self.get_checkout_source(request)

      try:
         if source == "cart":
            order = create_order_from_cart(
               user=request.user,
               shipping_address_id=shipping_address_id,
               shipping_method_id=shipping_method_id,
         )

         elif source == "buy_now":
            product_id = request.session.get(
               "buy_now_product_id"
            )
            quantity = request.session.get(
               "buy_now_quantity"
            )

            try:
               product_id = int(product_id)
               quantity = int(quantity)
            except (TypeError, ValueError):
               raise ValidationError(
                  "Your Buy Now session is invalid."
               )

            order = create_order_from_items(
               user=request.user,
               items=[
                  {
                     "product_id": product_id,
                     "quantity": quantity,
                  }
               ],
               shipping_address_id=shipping_address_id,
               shipping_method_id=shipping_method_id,
            )

         else:
            raise ValidationError("Invalid checkout source.")


      except ValidationError as exc:
         for error in exc.messages:
            messages.error(request, error)

         return redirect("orders:checkout")


      # Clear checkout session only after successful order creation.
      request.session.pop("shipping_method_id", None)
      request.session.pop("shipping_address_id", None)
      request.session.pop("checkout_source", None)
      request.session.pop("buy_now_product_id", None)
      request.session.pop("buy_now_quantity", None)

      messages.success(
         request,
         "Your order has been placed successfully.",
      )

      return redirect(
         "orders:detail",
         order_number=order.order_number,
      )

            



# Buy Now View
class BuyNowView(LoginRequiredMixin, View):
   def post(self, request, product_id):
      # 1. Read quantity from POST.
      try:
         quantity = int(request.POST.get("quantity", 1))
      except (TypeError, ValueError):
         messages.error(request, "Please enter a valid quantity.")
         return redirect(
            "products:detail", 
            slug="",
         )

      # 2. Validate quantity.
      if quantity < 1:
         messages.error(request, "Quantity must be at least 1.")
         return redirect(
            "products:detail",
            slug="",
         )

      # 3. Fetch the active product.
      product = Product.objects.filter(
         pk=product_id,
         is_active=True,
      ).first()

      if product is None:
         messages.error(request, "This product is unavailable.")
         return redirect("products:list")

      # 4. Validate stock.
      if product.stock < quantity:
         messages.error(
            request,
            f"Insufficient stock. Available: {product.stock}.",
         )
         return redirect(
            "products:detail",
            slug=product.slug,
         )

      # 5. Store the Buy Now intent in the session.
      request.session["checkout_source"] = "buy_now"
      request.session["buy_now_product_id"] = product.pk 
      request.session["buy_now_quantity"] = quantity

      # 6. Remove old shipping selection.
      request.session.pop("shipping_address_id", None)
      request.session.pop("shipping_method_id", None)

      messages.success(
         request,
         "Product selected. Please choose your delivery details.",
      )

      return redirect("shipping:options")




# OrderDetailView
class OrderDetailView(LoginRequiredMixin, DetailView):
   model = Order
   template_name = "orders/order_detail.html"
   context_object_name = "order"
   slug_field = "order_number"
   slug_url_kwarg = "order_number"

   def get_queryset(self):
      return (
         super().get_queryset()
         .filter(user=self.request.user)
         .prefetch_related("items")
      )

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["order_items"] = self.object.items.all()

      return context
   


# Order History View
class OrderHistoryView(LoginRequiredMixin, ListView):
   model = Order
   template_name = "orders/order_history.html"
   context_object_name = "orders"
   paginate_by = 10

   def get_queryset(self):
      return (
         Order.objects
         .filter(user=self.request.user)
         .prefetch_related("items")
         .order_by("-created_at")
      )