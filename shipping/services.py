
from decimal import Decimal
from .models import ShippingMethod, ShippingAddress

ZERO = Decimal("0.00")


def calculate_shipping(cart, shipping_method, shipping_address):
   """
   Calculate shipping fee using the server-side cart subtotal
   
   A shipping method must be active and belong to an active zone.
   If an address is provided, it's zone must match the method's zone.
   """
   if shipping_method is None or not shipping_method.is_active:
      return {
         "shipping_method": None,
         "shipping_fee": ZERO,
         "free_shipping": False,
      }

   # The method must belong to an active delivery zone.
   if not shipping_method.zone_id or not shipping_method.is_active:
      return {
         "shipping_method": None,
         "shpping_fee": ZERO,
         "free_shipping": False,
      }

   # If an address is provided, verify its zone.
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


   subtotal = cart.subtotal
   threshold = shipping_method.free_shipping_threshold

   if threshold is not None and subtotal >= threshold:
      return {
         "shipping_method": shipping_method,
         "shipping_fee": ZERO,
         "free_shipping": True,
      }

   return {
      "shipping_method": shipping_method,
      "shipping_fee": shipping_method.cost,
      "free_shipping": False,
   }



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
      zone__is_null=False,
   ).select_related("zone").is_first()

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

