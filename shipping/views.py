
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from carts.models import Cart
from .forms import ShippingMethodForm, ShippingAddressForm
from .models import ShippingZone



class ShippingOptionsView(LoginRequiredMixin, View):
   template_name = "shipping/shipping_options.html"

   def get_cart(self, user):
      return Cart.objects.filter(user=user).first()
      
   def render_forms(self, request, address_form, method_form):
      return render(
         request,
         self.template_name,
         {
            "address_form": address_form,
            "method_form": method_form,
         },
      )

   def get(self, request):
      cart = self.get_cart(request.user)

      if not cart or not cart.items.exists():
         messages.info(
            request,
            "Add a product to your cart before choosing delivery.",
         )
         return redirect(
            "carts:detial"
         )

      address_form = ShippingAddressForm(prefix="address")
      method_form = ShippingMethodForm(prefix="method")

      return self.render_forms(
         request,
         address_form,
         method_form,
      )



   def post(self, request):
      cart = self.get_cart(request.user)

      if not cart or not cart.items.exists():
         messages.error(
            request,
            "Your cart is empty"
         )
         return redirect(
            "carts:detail"
         )

      zone_id = request.POST.get("address-zone")

      zone = ShippingZone.objects.filter(
         pk=zone_id,
         is_active=True,
      ).first() if zone_id else None 

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
         "Shipping address and delivery method saved sucessfully.",
      )
      return redirect(
         "carts:detail"
      )

      
         

