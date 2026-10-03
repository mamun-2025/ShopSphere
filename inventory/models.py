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

   @property
   def is_low_stock(self):
      return self.product.stock <= self.low_stock_threshold

   @property
   def is_out_of_stock(self):
      return self.product.stock == 0

   @property
   def stock_status(self):
      if self.is_out_of_stock:
         return "Out of Stock"

      if self.is_low_stock:
         return "Low Stock"

      return "In Stock"


   # Stock Validation
   def validate_quantity(self, quantity):
      if quantity <= 0:
         raise ValueError(
            "Quantity must be greater than zero."
         )


   # Increase Stock
   def increase_stock(self, quantity):
      self.validate_quantity(quantity)

      self.product.stock += quantity

      self.product.save(
         update_fields=["stock"]
      )


   # Decrease Stock
   def decrease_stock(self, quantity):
      self.validate_quantity(quantity)

      if quantity > self.product.stock:
         raise ValueError(
            "Insufficient stock."
         )

      self.product.stock -= quantity

      self.product.save(
         update_fields=["stock"]
      )


   def __str__(self):
      return f"Inventory: {self.product.name}"

