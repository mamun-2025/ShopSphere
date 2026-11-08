
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from payments.services import start_sslcommerz_payment, identify_sslcommerz_callback


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

   logger.info(
      "SSLCommerz success callback received. "
      "Payment Reference: %s",
      payment.payment_reference,
   )

   # Do not mark payment as SUCCESS here.
   # Server-side verification is required.
   return HttpResponse(
      "Payment Response received."
      "Verification is pending",
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
