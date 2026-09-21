
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.db import models
from categories.models import Category

class Product(models.Model):
   name = models.CharField(max_length=100)

   slug = models.SlugField(
      max_length=220,
      unique=True,
   )

   category = models.ForeignKey(
      Category,
      on_delete=models.PROTECT,
      related_name="products",
   )

   brand = models.CharField(
      max_length=100,
      blank=True,
      null=True,
   )

   description = models.TextField(blank=True)

   sku = models.CharField(
      max_length=100,
      unique=True,
   )

   price = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      validators=[
         MinValueValidator(0)
      ],
   )

   stock = models.PositiveIntegerField(
      default=0,
   )

   is_active = models.BooleanField(
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


   def save(self, *args, **kwargs):

      if not self.slug:
         self.slug = slugify(self.name)

      super().save(*args, **kwargs)