from django.db import models
from products.models import Product


class Inventory(models.Model):

   product = models.OneToOneField(
      Product,
      on_delete=models.CASCADE,
      related_name="inventory",
   )

   low_stock_threshold = models.PositiveIntegerField(
      default=5,
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   def __str__(self):
      return f"Inventory: {self.product.name}"

