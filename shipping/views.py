
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from carts.models import Cart
from .forms import ShippingMethodForm, ShippingAddressForm



class ShippingOptionsView(LoginRequiredMixin, View):
   template_name = "shipping/shipping_options.html"

   def get(self, request):
      cart = Cart.objects.filter(user=request.user).first()

      if not cart or not cart.items.exists():
         messages.info(
            request,
            "Add a product to your cart before choosing delivery.",
         )
         return redirect(
            "carts:detail"
         )

      address_form = ShippingAddressForm(prefix="address")
      method_form = ShippingMethodForm(prefix="method")

      return render(
         request,
         self.template_name,
         {
            "address_form": address_form,
            "method_form": method_form,
         },
      )



   def post(self, request):
      cart = Cart.objects.filter(user=request.user).first()

      if not cart or not cart.items.exists():
         messages.error(
            request,
            "Your cart is empty"
         )
         return redirect(
            "carts:detail"
         )

      address_form = ShippingAddressForm(
         request.POST,
         prefix="address",
      )

      method_form = ShippingMethodForm(
         request.POST,
         prefix="method",
      )

      if address_form.is_valid() and method_form.is_valid():
         address = address_form.save(commit=False)
         address.user = request.user 
         address.save()

         shipping_method = method_form.cleaned_data[
            "shipping_method"
         ]

         request.session["shipping_address_id"] = address.pk 
         request.session["shipping_method_id"] = shipping_method.pk 

         messages.success(
            request,
            "Delivery address and shipping method saved.",
         )
         return redirect(
            "carts:detail"
         )

      return redirect(
         request,
         self.template_name,
         {
            "address_form": address_form,
            "method_form": method_form,
         },
         
      )