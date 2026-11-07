
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from decimal import Decimal


class Payment(models.Model):

   class Method(models.TextChoices):
      COD = "cod", "Cash on Delivery"
      SSLCOMMERZ = "sslcommerz", "SSLCommerz"
      BKASH = "bkash", "bkash"
      NAGAD = "nagad", "Nagad"

   class Status(models.TextChoices):
      PENDING = "pending", "Pending"
      PROCESSING = "processing", "Processing"
      SUCCESS = "success", "Success"
      FAILED = "failed", "Failed"
      CANCELLED = "cancelled", "Cancelled"
      REFUNDED = "refunded", "Refunded"


   payment_reference = models.UUIDField(
      default=uuid.uuid4,
      unique=True,
      editable=False,
   )

   order = models.ForeignKey(
      "orders.Order",
      on_delete=models.PROTECT,
      related_name="payments",
   )

   user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.PROTECT,
      related_name="payments",
   )

   amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[MinValueValidator(Decimal("0.01"))],
   )

   currency = models.CharField(
      max_length=3,
      default="BDT",
   )

   method = models.CharField(
      max_length=20,
      choices=Method.choices,
   )

   status = models.CharField(
      max_length=20,
      choices=Status.choices,
      default=Status.PENDING,
   )

   gateway_transaction_id = models.CharField(
      max_length=100,
      null=True,
      blank=True,
   )

   gateway_session_key = models.CharField(
      max_length=100,
      null=True,
      blank=True,
   )

   created_at = models.DateTimeField(
      auto_now_add=True,
   )

   updated_at = models.DateTimeField(
      auto_now=True,
   )

   class Meta:
      ordering = ["-created_at"]

      indexes = [
         models.Index(
            fields=["order", "status"],
            name="payment_order_status_idx",
         ),
         models.Index(
            fields=["user", "-created_at"],
            name="payment_user_created_idx",
         ),
      ]

      constraints = [
         models.CheckConstraint(
            condition=Q(amount__gt=0),
            name="payment_amount_gt_zero",
         ),
         models.UniqueConstraint(
            fields=["method", "gateway_transaction_id"],
            condition=(
               Q(gateway_transaction_id__isnull=False)
               & ~Q(gateway_transaction_id="")
            ),
            name="unique_gateway_transaction",
         ),
         models.UniqueConstraint(
            fields=["order"],
            condition=Q(
               status__in=["pending", "processing"]
            ),
            name="unique_active_payment_per_order",
         ),
         
      ]

   def __str__(self):
      return (
         f"{self.payment_reference}-"
         f"{self.get_status_display()}"
      )

   

