
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from payments.services import start_sslcommerz_payment


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


