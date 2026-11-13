

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Coupon

MONEY_PLACES = Decimal("0.01")

def normalize_coupon_code(code):
   """
   Normalize coupon code before database lookup.
   """
   if not isinstance(code, str) or not code.strip():
      raise ValidationError("Please enter a coupon code.")

   return code.strip().upper()




def validate_coupon_instance(
      *,
      coupon,
      user,
      subtotal,
      now=None,
):
   """
   Validate an already-fetched Coupon instance.

   During order creation, the coupon instance should
   be fetched using select_for_update().
   """
   if not user or not user.is_authenticated:
      raise ValidationError(
         "You must be logged in to use a coupon."
      )

   try:
      subtotal = Decimal(str(subtotal))
   except (InvalidOperation, TypeError, ValueError):
      raise ValidationError(
         "Invalid order amount."
      )

   if not subtotal.is_finite() or subtotal < Decimal("0.00"):
      raise ValidationError(
         "Invalid order amount."
      )

   
   now = now or timezone.now()

   if not coupon.is_active:
      raise ValidationError("This coupon is inactive.")

   if now < coupon.start_at:
      raise ValidationError("This coupon is not active yet.")

   if now >= coupon.end_at:
      raise ValidationError("This coupon has expired.")

   # 6. Check global usage limit 
   if (
      coupon.usage_limit is not None
      and coupon.used_count >= coupon.usage_limit
   ):
      raise ValidationError(
         "This coupon usage limit has been reached."
      )

   # 7. Check minimum order amount.
   if subtotal < coupon.minimum_order_amount:
      raise ValidationError(
         f"Minimum order amount is "
         f"{coupon.minimum_order_amount}"
      )

   # 8. Check per user usage limit
   previous_usage = coupon.usages.filter(
      user=user
   ).count()

   if previous_usage >= coupon.per_user_limit:
      raise ValidationError(
         "You have already used this coupon "
         "maximum allowed times."
      )

   return coupon




   
def validate_coupon(code, user, subtotal, now=None):

   if not isinstance(code, str) or not code.strip():
      raise ValidationError(
         "Please enter a coupon code."
      )
   
   normalized_code = normalize_coupon_code(code)

   coupon = Coupon.objects.filter(
      code=normalized_code
   ).first()

   if coupon is None:
      raise ValidationError(
         "Invalid coupon code."
      )

   return validate_coupon_instance(
      coupon=coupon,
      user=user,
      subtotal=subtotal,
      now=now,
   )




def calculate_coupon_discount(coupon, subtotal):
   """
   Calculate the actual discount amount.
   Returns:
   Decimal discount amount 
   """   

   try:
      subtotal = Decimal(str(subtotal))
   except (InvalidOperation, TypeError, ValueError):
      raise ValidationError("Invalid order amount.")

   if coupon.discount_type == Coupon.DiscountType.PERCENTAGE:
      discount = (
         subtotal * coupon.discount_value
      ) / Decimal("100")

      # Apply maximum discount limit 
      if coupon.maximum_discount is not None:
         discount = min(
            discount,
            coupon.maximum_discount,
         )

   elif coupon.discount_type == Coupon.DiscountType.FIXED:
      discount = coupon.discount_value

   else:
      raise ValidationError("Unsupported discount type.")

   # Discount cannot exceed subtotal
   discount = min(discount, subtotal)

   return discount.quantize(
      MONEY_PLACES,
      rounding=ROUND_HALF_UP,
   )



def validate_and_calculate_coupon(code, user, subtotal):
   """
   Validate coupon and calculate discount
   """

   coupon = validate_coupon(
      code=code,
      user=user,
      subtotal=subtotal,
   )

   discount = calculate_coupon_discount(
      coupon=coupon,
      subtotal=subtotal,
   )

   return {
      "coupon": coupon,
      "discount": discount,
      "subtotal": Decimal(str(subtotal)).quantize(
         MONEY_PLACES,
         rounding=ROUND_HALF_UP,
      ),
   }



