

import requests

from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

from django.conf import settings


# 1. SSLCommerz Base URLs
SANDBOX_BASE_URL = "https://sandbox.sslcommerz.com"
LIVE_BASE_URL = "https://securepay.sslcommerz.com"


# 2. Get Base URL
def get_sslcommerz_base_url():
   if settings.SSLCOMMERZ_IS_SANDBOX:
      return SANDBOX_BASE_URL

   return LIVE_BASE_URL


# 3. Get Initiate Payment API URL
def get_sslcommerz_initiate_url():
   base_url = get_sslcommerz_base_url()

   return f"{base_url}/gwprocess/v4/api.php"



# 4. SSLCommerz Session API Creation
def validate_payment_data(payment_data):

   try:
      amount = Decimal(
         str(payment_data["total_amount"])
      )

   except (KeyError, InvalidOperation, TypeError):
      raise ValueError("Invalid Payment Amount")

   if not amount.is_finite():
      raise ValueError("Invalid payment amount.")

   if not Decimal("10.00") <= amount <= Decimal("500000.00"):
      raise ValueError("Payment amount outside the allowed range.")

   if payment_data.get("currency") != "BDT":
      raise ValueError("Only BDT currency is supported.")

   tran_id = payment_data.get("tran_id")

   if (
      not isinstance(tran_id, str)
      or not tran_id
      or len(tran_id) > 30
   ):
      raise ValueError("Invalid transaction ID.")



# 5. Create Payment Session
def create_payment_session(*, payment_data):
   validate_payment_data(payment_data)

   payload = {
      **payment_data,
      "store_id": settings.SSLCOMMERZ_STORE_ID,
      "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
   }

   response = requests.post(
      get_sslcommerz_initiate_url(),
      data=payload,
      timeout=(5, 20),
   )

   response.raise_for_status()

   result = response.json()

   if not isinstance(result, dict):
      raise ValueError("Invalid gateway response.")

   if result.get("status") != "SUCCESS":
      raise ValueError(
         result.get(
            "failedreason",
            "Payment session creation failed."
         )
      )

   gateway_url = result.get("GatewayPageURL")

   if not gateway_url:
      raise ValueError("GatewayPageURL is missing.")

   parsed_url = urlparse(gateway_url)

   allowed_hosts = {
      "sandbox.sslcommerz.com",
      "securepay.sslcommerz.com",
   }

   if (
      parsed_url.scheme != "https"
      or parsed_url.hostname not in allowed_hosts
   ):
      raise ValueError("Untrusted gateway URL.")


   return result


