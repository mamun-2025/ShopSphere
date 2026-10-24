

from decimal import Decimal
from django.core.validators import (
   MaxValueValidator,
   MinValueValidator,
)
from django.db import models


class TaxRate(models.Model):
   name = models.CharField(
      max_length=100,
      default="Default Tax",
   )

   rate = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      default=Decimal("0.00"),
      validators=[
         MinValueValidator(Decimal("0.00")),
         MaxValueValidator(Decimal("100.00")),
      ],
      help_text="Enter the percentage, for example 5.00 for 5%.",
   )

   is_active = models.BooleanField(
      default=True,
   )

   is_default = models.BooleanField(
      default=True,
      help_text="Use the rate for taxable products.",
   )

   created_at = models.DateTimeField(auto_now_add=True)

   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ["-updated_at"]

   def __str__(self):
      return f"{self.name} ({self.rate}%)"
