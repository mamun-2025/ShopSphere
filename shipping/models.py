
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models



# Shipping_Method Model
class ShippingMethod(models.Model):
   name = models.CharField(
      max_length=100,
      unique=True,
   )

   description = models.CharField(
      max_length=255,
      blank=True,
   )

   cost = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      validators=[
         MinValueValidator(Decimal("0.00"))
      ],
   )

   free_shipping_threshold = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      null=True,
      blank=True,
      validators=[
         MinValueValidator(Decimal("0.00"))
      ],
      help_text=(
         "Free shipping applies when the eligible subtotal "
         "reaches this amount. Leave blank to disable. "
      ),
   )

   estimated_delivery_days = models.PositiveSmallIntegerField(
      default=3,
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
      ordering = ["cost", "name"]

   def __str__(self):
      return self.name 



# Shipping_Address Model
class ShippingAddress(models.Model):
   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="shipping_addresses",
   )

   full_name = models.CharField(max_length=150)
   phone = models.CharField(max_length=20)
   address_line = models.CharField(max_length=255)
   area = models.CharField(max_length=100)
   city_or_district = models.CharField(max_length=100)
   postal_code = models.CharField(max_length=20, blank=True)

   delivery_instructions = models.CharField(
      max_length=255,
      blank=True,
   )

   is_default = models.BooleanField(default=False)

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   class Meta:
      ordering = ["-is_default", "-updated_at"]

   def __str__(self):
      return f"{self.full_name} - {self.city_or_district}"





