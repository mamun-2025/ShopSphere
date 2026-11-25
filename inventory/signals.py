

from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product
from .models import Inventory


@receiver(post_save, sender=Product)
def create_product_inventory(
   sender,
   instance,
   created,
   **kwargs,
):
   if created:
      Inventory.objects.get_or_create(
         product=instance,
      )
