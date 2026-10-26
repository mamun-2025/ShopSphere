
from decimal import Decimal
from .models import ShippingMethod, ShippingAddress

ZERO = Decimal("0.00")


def calculate_shipping(cart, shipping_method):
   """
   Calculate shipping fee using the server-side cart subtotal
   and the selected active shipping method.
   """
   if shipping_method is None or not shipping_method.is_active:
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



def shipping_selection(request):
   """
   Load the current user's saved shipping selection from session.
   Invalid or outdated selections safety return an empty selcection.
   """
   method_id = request.session.get("shipping_method_id")
   address_id = request.session.get("shipping_address_id")

   method = None 
   address = None

   if method_id:
      method = ShippingMethod.objects.filter(
         pk=method_id,
         is_active=True,
      ).first()

   if address_id and request.user.is_authenticated:
      address = ShippingAddress.objects.filter(
         pk=address_id,
         user=request.user,
      ).first()

   return method, address

