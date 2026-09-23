
from django.utils.text import slugify
from django.core.validators import MinValueValidator, FileExtensionValidator
from .validators import validate_file_size
from django.db import models
from categories.models import Category



# Product Model
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

   # Main Product Image
   image = models.ImageField(
      upload_to="products/",
      blank=True,
      null=True,
   )

   # Product Manual Pdf 
   manual = models.FileField(
      upload_to="products/manuals/",
      validators=[
         FileExtensionValidator(
            allowed_extensions=["pdf"]
         ),
         validate_file_size,
      ],
      blank=True,
      null=True,
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



   # Main Product Replace and PDF Replace save method
   def save(self, *args, **kwargs):
      if self.pk:
         old_product = Product.objects.get(pk=self.pk)

         # Main product image replace
         if (
            old_product.image and old_product.image.name != self.image.name
         ): 
            old_product.image.delete(save=False)

         # PDF Replace
         if (
            old_product.manual and old_product.manual.name != self.manual.name 
         ):
            old_product.manual.delete(save=False)


      # Automatically slug method
      if not self.slug:
         self.slug = slugify(self.name)

      super().save(*args, **kwargs)


   # Main Product Delete Method
   def delete(self, *args, **kwargs):
      # Main Image delete
      if self.image:
         self.image.delete(save=False)

      # Pdf delete
      if self.manual:
         self.manual.delete(save=False)

      # Gallery images
      for product_image in self.images.all():
         product_image.delete()

      super().delete(*args, **kwargs)







# Product ImgaeModel
class ProductImage(models.Model):

   product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="images",
   )

   image = models.ImageField(
      upload_to="products/gallery/",
      blank=True,
      null=True,
   )

   alt_text = models.CharField(
      max_length=200,
      blank=True,
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   def __str__(self):
      return f"{ self.product.name } Image"


   # ProductImage Replace save method
   def save(self, *args, **kwargs):

      if self.pk:
         old_image = ProductImage.objects.get(pk=self.pk)

         if (
            old_image.image and old_image.image.name != self.image.name 
         ):
            old_image.image.delete(save=False)

      super().save(*args, **kwargs)


   # ProductImage Delete Method(Gallery)
   def delete(self, *args, **kwargs):
      if self.image:
         self.image.delete(save=False)

      super().delete(*args, **kwargs)



