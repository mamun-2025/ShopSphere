
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from carts.models import Cart
from products.models import Product 

from .forms import ShippingMethodForm, ShippingAddressForm
from .models import ShippingZone



class ShippingOptionsView(LoginRequiredMixin, View):
   template_name = "shipping/shipping_options.html"

   def get_checkout_source(self, request):
      return request.session.get("checkout_source", "cart")

   def validate_checkout_source(self, request):
      """
      Validate either Cart Checkout or Buy Now Checkout.
      Does not modify Cart or Wishlist.
      """

      source = self.get_checkout_source(request)

      if source == "cart":
         cart = Cart.objects.filter(
            user=request.user
         ).first()

         if not cart or not cart.items.exists():
            return False, "Your cart is empty."

         stock_issues = cart.get_stock_issues()

         if stock_issues:
            return False, "Please resolve stock issues in your cart."

         return True, None 

      if source == "buy_now":
         product_id = request.session.get("buy_now_product_id")
         quantity = request.session.get("buy_now_quantity")

         try:
            quantity = int(quantity)
            product_id = int(product_id)
         except (TypeError, ValueError):
            return False, "Your Buy Now session is invalid. Please try again."

         if quantity <= 1:
            return False, "Invalid product quantity for Buy Now checkout."

         product = Product.objects.filter(
            pk=product_id,
            is_active=True,
         ).first()

         if product is None:
            return False, "The product is no longer available."

         if product.stock < quantity:
            return False, (
               f"Insufficient stock for {product.name}."
               f"Available stock: {product.stock}."
            )

         return True, None 

      return False, "Invalid checkout session."


   def render_forms(self, request, address_form, method_form):
      return render(
         request,
         self.template_name,
         {
            "address_form": address_form,
            "method_form": method_form,
            "checkout_source": self.get_checkout_source(request),
         },
      )


   def get(self, request):
      valid, error = self.validate_checkout_source(request)

      if not valid:
         messages.error(request, error)

         if self.get_checkout_source(request) == "buy_now":
            request.session.pop("checkout_source", None)
            request.session.pop("buy_now_product_id", None)
            request.session.pop("buy_now_quantity", None)

         return redirect("carts:detail")

      address_form = ShippingAddressForm(prefix="address")
      method_form = ShippingMethodForm(prefix="method")

      return self.render_forms(
         request,
         address_form,
         method_form,
      )



   def post(self, request):
      valid, error = self.validate_checkout_source(request)

      if not valid:
         messages.error(request, error)
         return redirect("shipping:options")

      zone_id = request.POST.get("address-zone")

      zone = (
         ShippingZone.objects.filter(
         pk=zone_id,
         is_active=True,
         ).first() 
         if zone_id 
         else None 
      )

      address_form = ShippingAddressForm(
         request.POST,
         prefix="address",
      )

      method_form = ShippingMethodForm(
         request.POST,
         prefix="method",
         zone=zone,
      )

      address_valid = address_form.is_valid()
      method_valid = method_form.is_valid()

      if not address_valid or not method_valid:
         return self.render_forms(
            request,
            address_form,
            method_form,
         )

      address = address_form.save(commit=False)
      address.user = request.user

      if not zone or address.zone_id != zone.pk:
         address_form.add_error(
            "zone",
            "Please select a valid delivery zone",
         )
         return self.render_forms(
            request,
            address_form,
            method_form,
         )

      shipping_method = method_form.cleaned_data["shipping_method"]

      if shipping_method.zone_id != address.zone_id:
         method_form.add_error(
            "shipping_method",
            "The shipping method does not match your delivery zone.",
         )
         return self.render_forms(
            request,
            address_form,
            method_form,
         )

      try:
         address.full_clean()
         address.save()

      except ValidationError as exc:
         for field, errors in exc.message_dict.items():
            for error in errors:
               if field in address_form.fields:
                  address_form.add_error(field, error)
               else:
                  address_form.add_error(None, error)

         return self.render_forms(
            request,
            address_form,
            method_form,
         )

      request.session["shipping_address_id"] = address.pk
      request.session["shipping_method_id"] = shipping_method.pk 

      messages.success(
         request,
         "Shipping address and delivery method saved successfully.",
      )
      return redirect(
         "carts:detail"
      )

      
         

