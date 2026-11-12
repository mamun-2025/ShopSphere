
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings


class Coupon(models.Model):

   class DiscountType(models.TextChoices):
      PERCENTAGE = "percentage", "Percentage"
      FIXED = "fixed", "Fixed"

   # coupon code
   code = models.CharField(
      max_length=50,
      unique=True,
      db_index=True,
   ) 

   # Discount configuration
   discount_type = models.CharField(
      max_length=20,
      choices=DiscountType.choices,
   )

   discount_value = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[
         MinValueValidator(Decimal("0.01")),
      ],
   )

   # Order Amount Rules 
   minimum_order_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=Decimal("0.00"),
      validators=[
         MinValueValidator(Decimal("0.00")),
      ],
   )

   maximum_discount = models.DecimalField(
      max_digits=12,
      decimal_places=2, 
      null=True,
      blank=True,
      validators=[
         MinValueValidator(Decimal("0.01")),
      ],
   )

   # Validity Period
   start_at = models.DateTimeField()

   end_at = models.DateTimeField()

   # Usage Limits 
   usage_limit = models.PositiveIntegerField(
      null=True,
      blank=True,
   )

   used_count = models.PositiveIntegerField(
      default=0,
   )

   per_user_limit = models.PositiveIntegerField(
      default=1,
      validators=[
         MinValueValidator(1),
      ],
   )

   is_active = models.BooleanField(
      default=True,
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   class Meta:
      ordering = ["-created_at"]

      constraints = [
         models.CheckConstraint(
            condition=Q(used_count__gte=0),
            name="coupon_used_count_nonnegative",
         ),
         models.CheckConstraint(
            condition=(
               Q(usage_limit__isnull=True)
               | Q(used_count__lte=models.F("usage_limit"))
            ),
            name="coupon_usage_within_limit",
         ),
      ]

      indexes = [
         models.Index(
            fields=["code", "is_active"],
            name="coupon_code_active_idx",
         ),
         models.Index(
            fields=["start_at", "end_at"],
            name="coupon_validity_idx",
         ),
      ]

   def clean(self):
      super().clean()

      # Normalize Coupon Code
      if self.code:
         self.code = self.code.strip().upper() 

      # Validate Discount Value
      if self.discount_value is not None:
         if self.discount_type == self.DiscountType.PERCENTAGE:
            if self.discount_value > Decimal("100"):
               raise ValidationError({
                  "discount_value":
                     "Percentage discount cannot exceed 100%."
               })

      
      # Validate Maximum Discount
      if (
         self.maximum_discount is not None
         and self.discount_type != self.DiscountType.PERCENTAGE
      ):
         raise ValidationError({
            "maximum_discount":
               "Maximum discount is only applicable to percentage coupons."
         })

      # Validate Date Range
      if (
         self.start_at is not None
         and self.end_at is not None
         and self.end_at <= self.start_at
      ):
         raise ValidationError({
            "end_at":
               "Expiration date must be later than start date."
         })

      # Validate Usage Limit 
      if (
         self.usage_limit is not None
         and self.used_count > self.usage_limit
      ):
         raise ValidationError({
            "usage_limit":
               "Usage limit cannot be lower than used count."
         })

   def save(self, *args, **kwargs):
      if self.code:
         self.code = self.code.strip().upper()

      super().save(*args, **kwargs)


   @property
   def is_expired(self):
      return timezone.now() >= self.end_at 

   @property
   def is_available(self):
      now = timezone.now()

      return (
         self.is_active
         and self.start_at <= now < self.end_at
         and (
            self.usage_limit is None 
            or self.used_count < self.usage_limit
         )
      )

   def __str__(self):
      return self.code 




class CouponUsage(models.Model):
   coupon = models.ForeignKey(
      Coupon,
      on_delete=models.PROTECT,
      related_name="usages",
   )

   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      related_name="coupon_usages",
   )

   order = models.OneToOneField(
      "orders.Order",
      on_delete=models.PROTECT,
      related_name="coupon_usage",
   )

   used_at = models.DateTimeField(
      auto_now_add=True
   )

   class Meta:
      ordering = ["-used_at"]

      indexes = [
         models.Index(
            fields=["coupon", "user"],
            name="coupon_user_usage_idx",
         ),
      ]

   def __str__(self):
      return f"{self.coupon.code} - {self.user}"