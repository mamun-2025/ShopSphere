

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