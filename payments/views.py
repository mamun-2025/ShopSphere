
import logging
import requests

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from payments.services import start_sslcommerz_payment, identify_sslcommerz_callback, verify_sslcommerz_payment

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Payment



@login_required
@require_POST
def sslcommerz_payment_start(request, order_id):
   try:
      result = start_sslcommerz_payment(
         order_id=order_id,
         user=request.user,
      )

   except ValidationError as exc:
      return HttpResponseBadRequest(
         str(exc)
      )

   return redirect(result["gateway_url"])



# Create Success Callback
logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def sslcommerz_success(request):
   try:
      payment = identify_sslcommerz_callback(
         callback_data=request.POST,
      )

   except ValidationError:
      return HttpResponseBadRequest(
         "Invalid payment callback."
      )

   val_id = request.POST.get("val_id")

   if not val_id:
      return HttpResponseBadRequest(
         "Missing Validation ID."
      )

   try: 
      payment = verify_sslcommerz_payment(
         tran_id=payment.gateway_transaction_id,
         val_id=val_id,
      )

   except ValidationError:
      logger.warning(
         "SSLCommerz payment verification failed. "
         "Payment Reference: %s",
         payment.payment_reference,
      )

      return HttpResponse(
         "Payment verification failed.",
         status=400,
      )

   except Exception:
      logger.exception(
         "SSLCommerz verification error. "
         "Payment Reference: %s",
         payment.payment_reference,
      )

      return HttpResponse(
         "Payment verification is pending.",
         status=503,
      )

   logger.info(
      "SSLCommerz payment verification completed. "
      "Payment Reference: %s, Status: %s",
      payment.payment_reference,
      payment.status,
   )

   # Do not mark payment as SUCCESS here.
   # Server-side verification is required.
   return HttpResponse(
      "Payment Response received."
      "Verification status: "
      f"{payment.status}",
      status=200,
   )


# Create Failed Callback
@csrf_exempt
@require_POST
def sslcommerz_fail(request):
   try:
      payment = identify_sslcommerz_callback(
         callback_data=request.POST,
      )

   except ValidationError:
      return HttpResponseBadRequest(
         "Invalid Payment Callback."
      )

   logger.info(
      "SSLCommerz failed callback received."
      "Payment Reference: %s",
      payment.payment_reference,
   )

   # Do not update payment status from
   # unverified browser callback data.
   return HttpResponse(
      "Gateway reported a payment fialure. "
      "Payment status is awaiting verification.",
      status=200,
   )



# Create Cancel Callback
@csrf_exempt
@require_POST
def sslcommerz_cancel(request):
   try:
      payment = identify_sslcommerz_callback(
         callback_data=request.POST, 
      )

   except ValidationError:
      return HttpResponseBadRequest(
         "Invalid payment callback."
      )

   logger.info(
      "SSLCommerz cancel callback received. "
      "Payment Reference: %s",
      payment.payment_reference,
   )

   # Do not mark the payment as CANCELLED
   # until its final status is established.
   return HttpResponse(
      "Payment cancellation received. "
      "Payment status is awaiting verification.",
      status=200,
   )



# Create SSLCommerz IPN View
@csrf_exempt
@require_POST
def sslcommerz_ipn(request):

   # 1. Recieve IPN data from sslcommerz
   callback_status = request.POST.get("status")
   tran_id = request.POST.get("tran_id")
   val_id = request.POST.get("val_id")

   # 2. Validate required fields 
   if not tran_id or not val_id or not callback_status:

      logger.warning(
         "Invalid SSLCommerz IPN notification received."
      )

      return HttpResponseBadRequest(
         "Invalid IPN notification"
      )

   # 3. Handle non-success notifications
   if callback_status not in {"VALID", "VALIDATED"}:

      logger.info(
         "SSLCommerz IPN received with non-success status."
         "Transaction ID: %s, Status: %s",
         tran_id,
         callback_status,
      )

      # Do not mark payment as FAILED or CANCELLED 
      # based only on an unverified notifiction.

      return HttpResponse(
         "IPN notification received.",
         status=200,
      )

   # 4. Verify payment through SSLCommerz Validation API
   try:
      payment = verify_sslcommerz_payment(
         tran_id=tran_id,
         val_id=val_id,
      )

   except ValidationError:
      logger.warning(
         "SSLCommerz IPN verification rejected. "
         "Transaction ID: %s",
         tran_id,
      )

      return HttpResponse(
         "IPN verification failed.",
         status=400,
      )

   except (
      requests.RequestException,
      ValueError,
   ):
      logger.exception(
         "SSLCommerz IPN verification temporarily failed. "
         "Transaction ID: %s",
         tran_id,
      )

      # Gateway/network response is uncertain.
      # Keep the existing payment status unchanged.

      return HttpResponse(
         "Payment verification temporarily unavailable.",
         status=503,
      )

   # 5. Log verified payment information
   logger.info(
      "SSLCommerz IPN processes successfully."
      "Payment Reference: %s, Status: %s",
      payment.payment_reference,
      payment.status,
   )

   # 6. Acknowlege IPN notification
   return HttpResponse(
      "IPN notification processed successfully.",
      status=200,
   )



# Admin Payment List View
class AdminPaymentListView(
   LoginRequiredMixin,
   UserPassesTestMixin,
   ListView,
): 
   model = Payment
   template_name = "payments/admin/payment_list.html"
   context_object_name = "payments"
   paginate_by = 10

   def test_func(self):
      return self.request.user.is_superuser

   def get_queryset(self):
      queryset = (
         Payment.objects
         .select_related("user", "order")
         .order_by("-created_at")
      )

      search_query = self.request.GET.get(
         "q", ""
      ).strip()

      if search_query:
         queryset = queryset.filter(
            Q(gateway_transaction_id__icontains=search_query)
            | Q(user__username__icontains=search_query)
            | Q(user__email__icontains=search_query)
         )

      status_filter = self.request.GET.get(
         "status", ""
      )

      valid_statuses = dict(Payment.Status.choices)

      if status_filter in valid_statuses:
         queryset = queryset.filter(
            status=status_filter
         )

      method_filter = self.request.GET.get(
         "method", ""
      )

      valid_methods = dict(Payment.Method.choices)

      if method_filter in valid_methods:
         queryset = queryset.filter(
            method=method_filter
         )

      return queryset

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["search_query"] = self.request.GET.get("q", "")
      context["status_filter"] = self.request.GET.get("status", "")
      context["method_filter"] = self.request.GET.get("method", "")
      context["status_choices"] = Payment.Status.choices
      context["method_choices"] = Payment.Method.choices
      context["total_payments"] = Payment.objects.count()

      return context



# Admin Payment Detail View
class AdminPaymentDetailView(
   LoginRequiredMixin,
   UserPassesTestMixin,
   DetailView,
):
   model = Payment
   template_name = "payments/admin/payment_detail.html"
   context_object_name = "payment"

   def test_func(self):
      return self.request.user.is_superuser

   def get_queryset(self):
      return Payment.objects.select_related("user", "order")
   