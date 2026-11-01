
from decimal import Decimal
from .models import ShippingMethod, ShippingAddress

ZERO = Decimal("0.00")


def calculate_shipping_for_subtotal(
      subtotal,
      shipping_method,
      shipping_address=None,
):
   """
   Calculate shipping fee based on subtotal and shipping method.

   Works for both Cart Checkout and Buy Now Checkout.
   Subtotal means product value before tax.
   """
   if (
      shipping_method is None
      or not shipping_method.is_active
      or not shipping_method.zone_id
      or not shipping_method.zone.is_active 
   ):
      return {
         "shipping_method": None,
         "shipping_fee": ZERO,
         "free_shipping": False,
      }


   if shipping_address is not None:
      if (
         not shipping_address.zone_id
         or not shipping_address.zone.is_active
         or shipping_method.zone_id != shipping_address.zone_id
      ):
         return {
            "shipping_method": None,
            "shipping_fee": ZERO,
            "free_shipping": False,
         }

   subtotal = Decimal(str(subtotal))
   threshold = shipping_method.free_shipping_threshold 

   if threshold is not None and subtotal >= threshold:
      return {
         "shipping_method": shipping_method,
         "shipping_fee": ZERO,
         "free_shipping": True, 
      }

   return {
      "shipping_method": shipping_method,
      "shipping_fee": Decimal(str(shipping_method.cost)),
      "free_shipping": False,
   }


def calculate_shipping(cart, shipping_method, shipping_address=None):
   """
   Backward-compatible wrapper for existing Cart Checkout and Buy Now Checkout code.
   """
   if cart is None:
      subtotal = ZERO 
   else:
      subtotal = cart.subtotal 


   return calculate_shipping_for_subtotal(
      subtotal=subtotal,
      shipping_method=shipping_method,
      shipping_address=shipping_address,
   )




def get_shipping_selection(request):
   """
   Load the current user's shipping selection from session.

   Reject inactive methods, inactive zones, invalid address,
   and shipping method/address zone mismatches.
   """
   method_id = request.session.get("shipping_method_id")
   address_id = request.session.get("shipping_address_id")

   if not method_id or not address_id:
      return None, None

   if not request.user.is_authenticated:
      return None, None

   method = ShippingMethod.objects.filter(
      pk=method_id,
      is_active=True,
      zone__is_active=True,
      zone__isnull=False,
   ).select_related("zone").first()

   address = ShippingAddress.objects.filter(
      pk=address_id,
      user=request.user,
      zone__is_active=True,
   ).select_related("zone").first()

   if method is None or address is None:
      return None, None

   if method.zone_id != address.zone_id:
      return None, None

   return method, address

