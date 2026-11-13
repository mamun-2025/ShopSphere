
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views import View

from orders.views import CheckoutView
from taxes.services import calculate_items_totals

from .forms import CouponApplyForm
from .services import validate_and_calculate_coupon



class ApplyCouponView(LoginRequiredMixin, CheckoutView):

   def post(self, request, *args, **kwags):

      form = CouponApplyForm(request.POST)

      if not form.is_valid():
         messages.error(
            request,
            "Please enter a valid coupon.",
         )
         return redirect("orders:checkout")

      # Remove the previous coupon before applying a new one.
      request.session.pop("coupon_code", None)

      try:
         checkout_items = self.get_checkout_items(request)

         tax_summary = calculate_items_totals(
            checkout_items
         )

         subtotal = tax_summary["subtotal"]

         result = validate_and_calculate_coupon(
            code=form.cleaned_data["code"],
            user=request.user,
            subtotal=subtotal,
         )

         request.session["coupon_code"] = (
            result["coupon"].code 
         )

         messages.success(
            request,
            (
               f"Coupon {result["coupon"].code}"
               f"applied successfully. "
               f"You saved ৳{result["discount"]}"
            )
         )

      except ValidationError as exc:
         for error in exc.messages:
            messages.error(request, error)

      return redirect("orders:checkout")



class RemoveCouponView(LoginRequiredMixin, View):

   def post(self, request, *args, **kwargs):

      request.session.pop("coupon_code", None)

      messages.success(
         request,
         "Coupon removed successfully.",
      )

      return redirect("orders:checkout")


