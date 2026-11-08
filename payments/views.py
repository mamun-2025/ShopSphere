
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from payments.services import start_sslcommerz_payment, indentify_sslcommerz_callback


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
      payment = indentify_sslcommerz_callback(
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


