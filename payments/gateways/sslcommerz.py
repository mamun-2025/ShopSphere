

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

   if amount.as_tuple().exponent < -2:
      raise ValueError(
         "Payment amount cannot have more than 2 decimal places."
      )

   if not Decimal("10.00") <= amount <= Decimal("500000.00"):
      raise ValueError(
         "Payment amount outside the allowed range."
      )

   if payment_data.get("currency") != "BDT":
      raise ValueError(
         "Only BDT currency is supported."
      )

   tran_id = payment_data.get("tran_id")

   if (
      not isinstance(tran_id, str)
      or not tran_id.strip()
      or len(tran_id) > 30
   ):
      raise ValueError("Invalid transaction ID.")


# 5. Validate Gateway URL
def validate_gateway_url(gateway_url):

   if not isinstance(gateway_url, str):
      raise ValueError("Invalid gateway URL.")

   parsed_url = urlparse(gateway_url)

   allowed_hosts = {
      "sandbox.sslcommerz.com",
      "securepay.sslcommerz.com",
   }

   if (
      parsed_url.scheme != "https"
      or parsed_url.hostname not in allowed_hosts
      or parsed_url.port not in (None, 443)
      or parsed_url.username is not None
      or parsed_url.password is not None
   ):
      raise ValueError("Untrusted gateway URL.")

   return gateway_url



# 6. Create Payment Session
def create_payment_session(*, payment_data):

   validate_payment_data(payment_data)

   payload = {
      **payment_data,
      "store_id": settings.SSLCOMMERZ_STORE_ID,
      "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
   }

   # DEBUG: Check outgoing callback URLs
   print("\n========== OUTGOING SSLCommerz CALLBACK URLs ==========")

   print("SUCCESS URL:", payload.get("success_url"))
   print("FAIL URL:", payload.get("fail_url"))
   print("CANCEL URL:", payload.get("cancel_url"))
   print("IPN URL:", payload.get("ipn_url"))

   print("=======================================================\n")

   response = requests.post(
      get_sslcommerz_initiate_url(),
      data=payload,
      timeout=(5, 20),
   )

   response.raise_for_status()

   try:
      result = response.json()
   except requests.exceptions.JSONDecodeError as exc:
      raise ValueError(
         "Invalid response received from payment gateway."
      ) from exc 
   
   if not isinstance(result, dict):
      raise ValueError("Invalid gateway response.")

   if result.get("status") != "SUCCESS":

      reason = result.get("failedreason")

      if not isinstance(reason, str) or not reason:
         reason = "Payment session creation failed."

      raise ValueError(reason)
   

   gateway_url = result.get("GatewayPageURL")

   if not gateway_url:
      raise ValueError("GatewayPageURL is missing.")

   validate_gateway_url(gateway_url)

   if not result.get("sessionkey"):
      raise ValueError("Gateway session key is missing.")

   return result

   

# 7. Get Validation API URL 
def get_sslcommerz_validation_url():

   base_url = get_sslcommerz_base_url()

   return (
      f"{base_url}/validator/api/validationserverAPI.php"
   )


# 8. Validate SSLCommerz Transaction
def validate_sslcommerz_transaction(*, val_id):

   if not isinstance(val_id, str) or not val_id.strip():
      raise ValueError("Invalid Validation ID.")

   params = {
      "val_id": val_id,
      "store_id": settings.SSLCOMMERZ_STORE_ID,
      "store_passwd": settings.SSLCOMMERZ_STORE_PASSWORD,
      "format": "json",
   }

   response = requests.get(
      get_sslcommerz_validation_url(),
      params=params,
      timeout=(5, 20),
   )

   response.raise_for_status()

   try:
      result = response.json()
   except requests.exceptions.JSONDecodeError as exc:
      raise ValueError(
         "Invalid validation response from SSLCommerz."
      ) from exc 

   if not isinstance(result, dict):
      raise ValueError(
         "Unexpected validation response."
      )

   return result
