
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone



# Order model
class Order(models.Model):

   class Status(models.TextChoices):
      PENDING = "pending", "Pending"
      CONFIRED = "confirmed", "Confirmed"
      PROCESSING = "processing", "Processing"
      SHIPPED = "shipped", "Shipped"
      DELIVERED = "delivered", "Delivered"
      CANCELLED = "cancelled", "Cancelled"

   class PaymentMethod(models.TextChoices):
      COD = "cod", "Cash on Delivery"

   class PaymentStatus(models.TextChoices):
      UNPAID = "unpaid", "Unpaid"
      PAID = "paid", "Paid"
      REFUNDED = "refunded", "Refunded"

   order_number = models.UUIDField(
      default=uuid.uuid4,
      unique=True,
      editable=False,
   )

   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      related_name="orders",
   )

   status = models.CharField(
      max_length=20,
      choices=Status.choices,
   )

   payment_method = models.CharField(
      max_length=20,
      choices=PaymentMethod.choices,
      default=PaymentMethod.COD,
   )

   payment_status = models.CharField(
      max_length=20,
      choices=PaymentStatus.choices,
      default=PaymentStatus.UNPAID,
   )

   # Delivery address snapshot: preserves the address at checkout.
   shipping_full_name = models.CharField(max_length=150)
   shipping_phone = models.CharField(max_length=20)
   shipping_address_line = models.CharField(max_length=255)
   shipping_area = models.CharField(max_length=100)
   shipping_city_or_district = models.CharField(max_length=100)
   shipping_postal_code = models.CharField(
      max_length=20, 
      blank=True,
   )

   shipping_instructions = models.CharField(
      max_length=255,
      blank=True,
   )

   shipping_method_name = models.CharField(max_length=100)
   estimated_delivery_days = models.PositiveSmallIntegerField(
      default=3,
   )

   subtotal = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[
         MinValueValidator(0)
      ],
   )

   tax_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=0,
      validators=[
         MinValueValidator(0)
      ],
   )

   shipping_fee = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=0,
      validators=[
         MinValueValidator(0)
      ],   
   )

   total = models.DecimalField(
      max_digits=12,
      decimal_places=2, 
      validators=[
         MinValueValidator(0)
      ],
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
      return f"Order {self.order_number}"

   



