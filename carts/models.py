
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from products.models import Product


# Cart Model
class Cart(models.Model):

   user = models.OneToOneField(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name="cart",
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   @property
   def subtotal(self):
      return sum(
         item.product.price * item.quantity
         for item in self.items.select_related("product")
      )


   def get_stock_issues(self):

      issues = []

      cart_items = self.items.select_related("product")

      for item in cart_items:

         product = item.product

         if not product.is_active:
            issues.append(
               f"{product.name} is no longer available."
            )

         elif product.stock == 0:
            issues.append(
               f"{product.name} is out of stock."
            )

         elif item.quantity > product.stock:
            issues.append(
               f"{product.name}: only"
               f"{product.stock} item's available."
            )

      return issues


   def __str__(self):
      return f"Cart- {self.user.username}"

   

# CartItem Model
class CartItem(models.Model):

   cart = models.ForeignKey(
      Cart,
      on_delete=models.CASCADE,
      related_name="items",
   )

   product = models.ForeignKey(
      Product,
      on_delete=models.CASCADE,
      related_name="cart_items",
   )

   quantity = models.PositiveIntegerField(
      default=1,
      validators=[
         MinValueValidator(1),
      ],
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   class Meta:
      constraints = [
         models.UniqueConstraint(
            fields=["cart", "product"],
            name="unique_cart_product",
         ),
      ]

   def __str__(self):
      return f"{self.product.name } X {self.quantity}"



