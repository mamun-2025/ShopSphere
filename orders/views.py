
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from products.models import Product
from carts.models import Cart
from shipping.services import calculate_shipping, get_shipping_selection
from taxes.services import calculate_cart_totals

from .models import Order
from .services import create_order_from_cart


# CheckOut View
class CheckoutView(LoginRequiredMixin, View):
   template_name = "orders/checkout.html"

   def get(self, request):
      cart = Cart.objects.filter(
         user=request.user
      ).first()

      if not cart or not cart.items.exists():
         messages.info(
            request,
            "Your cart is empty."
         )
         return redirect(
            "carts:detail"
         )

      stock_issues = cart.get_stock_issues()

      if stock_issues:
         messages.error(
            request,
            "Please resolve stock issues before checkout.",
         )
         return redirect(
            "carts:detail"
         )

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

      tax_summary = calculate_cart_totals(cart)
      shipping_summary = calculate_shipping(
         cart,
         shipping_method,
         shipping_address,
      )

      service_fee = Decimal("0.00")
      shipping_fee = shipping_summary["shipping_fee"]

      total = (
         tax_summary["total"]
         + shipping_fee,
         + service_fee,
      )

      context = {
         "cart": cart,
         "cart_items": cart.items.select_related("product"),

         "shipping_method": shipping_method,
         "shipping_address": shipping_address,

         "shipping_fee": shipping_summary["shipping_fee"],
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

      try:
         order = create_order_from_cart(
            user=request.user,
            shipping_address_id=shipping_address_id,
            shipping_method_id=shipping_method_id,
         )
      except ValidationError as exc:
         for error in exc.messages:
            messages.error(
               request,
               error,
            )
         return redirect(
            "orders:checkout"
         )

      # Clear the selection only after the order is created.
      request.session.pop("shipping_method_id", None)
      request.session.pop("shipping_address_id", None)

      messages.success(
         request,
         "Your order has been placed.",
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
   


   