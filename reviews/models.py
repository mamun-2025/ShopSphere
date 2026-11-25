from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

class Review(models.Model):

   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="reviews",
   )

   product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="reviews",
   )

   rating = models.PositiveIntegerField(
      validators=[
         MinValueValidator(1),
         MaxValueValidator(5),
      ]
   )

   comment = models.TextField()

   is_active = models.BooleanField(default=True)

   created_at = models.DateTimeField(auto_now_add=True)

   updated_at = models.DateTimeField(auto_now=True)

   class Meta:
      ordering = ["-created_at"]

      constraints = [
         models.UniqueConstraint(
            fields = ["user", "product"],
            name="unique_user_product_review",
         ),
         models.CheckConstraint(
            condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
            name="review_rating_between_1_and_5",
         ),

      ]


   def __str__(self):
      return f"{self.user.username} - {self.product.name}"
