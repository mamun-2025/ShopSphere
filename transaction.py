

from django.db import transaction
from django.db.models import F 

from products.models import Product
from orders.models import Order

def purchase_product(customer, product_id):
   
   with transaction.atomic():

      updated = Product.objects.filter(
         id=product_id,
         stock__gt=0,
      ).update(
         stock=F("stock") - 1
      )

      if updated != 1:
         return None

      order = Order.objects.create(
         customer=customer

      )

      return order 
