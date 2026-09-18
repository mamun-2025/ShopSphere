from django.db import models
from categories.models import Category

class Product(models.Model):
   name = models.CharField(max_length=100)

   category = models.ForeignKey(
      Category,
      on_delete=models.PROTECT,
      related_name="products",
   )

   description = models.TextField(blank=True)

   sku = models.CharField(
      max_length=100,
      unique=True,
   )

   price = models.DecimalField(
      max_digits=10,
      decimal_places=2,
   )

   stock = models.PositiveIntegerField(
      default=0,
   )

   is_acitve = models.BooleanField(
      default=True,
   )

   created_at = models.DateTimeField(
      auto_now_add=True
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   class Meta:
      ordering = ["-created_at"]

   def __str__(self):
      return self.name 