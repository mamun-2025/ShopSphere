
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

ZERO = "0.00"


class Invoice(models.Model):

   class PaymentStatus(models.TextChoices):
      UNPAID = "unpaid", "Unpaid"
      PAID = "paid", "Paid"
      REFUNDED = "refunded", "Refunded"

   # One Order = One Invoice
   order = models.OneToOneField(
      "orders.Order",
      on_delete=models.PROTECT,
      related_name="invoice",
   )

   invoice_number = models.CharField(
      max_length=40,
      unique=True,
      editable=False,
   )

   issued_at = models.DateTimeField(
      default=timezone.now, 
      editable=False,
   )

   # Customer snapshot
   customer_name = models.CharField(
      max_length=150,
   )

   customer_email = models.EmailField(
      blank=True,
      default="",
   )

   customer_phone = models.CharField(
      max_length=20,
   )

   # Shipping address snapshot
   shipping_address_line = models.CharField(
      max_length=255,
   )

   shipping_area = models.CharField(
      max_length=100,
   )

   shipping_city_or_district = models.CharField(
      max_length=100,
   )

   shipping_postal_code = models.CharField(
      max_length=20,
      blank=True,
      default="",
   )

   shippng_zone_name = models.CharField(
      max_length=100,
      blank=True,
      default="",
   )

   shipping_method_name = models.CharField(
      max_length=100,
   )

   # Payment snapshot
   payment_method = models.CharField(
      max_length=20,
   )

   payment_status = models.CharField(
      max_length=20,
      choices=PaymentStatus.choices,
      default=PaymentStatus.UNPAID,
   )

   # Financial snapshots
   subtotal = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[
         MinValueValidator(0),
      ],
   )

   tax_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   shipping_fee = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   service_fee = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   coupon_code = models.CharField(
      max_length=50,
      blank=True,
      default="",
   )

   discount_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   total = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[
         MinValueValidator(0),
      ],
   )

   created_at = models.DateTimeField(
      auto_now_add=True
   )

   class Meta:
      ordering = ["-issued_at"]

   def __str__(self):
      return self.invoice_number



class InvoiceItem(models.Model):

   invoice = models.ForeignKey(
      Invoice,
      on_delete=models.CASCADE,
      related_name="items",
   )

   product = models.ForeignKey(
      "products.Product",
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name="invoice_items",
   )

   product_name = models.CharField(
      max_length=255,
   )

   unit_price = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      validators=[
         MinValueValidator(0),
      ],
   )

   quantity = models.PositiveIntegerField(
      validators=[
         MinValueValidator(1),
      ],
   )

   is_taxable = models.BooleanField(
      default=True,
   )

   tax_rate = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   tax_amount = models.DecimalField(
      max_digits=12,
      decimal_places=2,
      default=ZERO,
      validators=[
         MinValueValidator(0),
      ],
   )

   line_total = models.DecimalField(
      max_digits=12,
      decimal_places=2, 
      validators=[
         MinValueValidator(0),
      ],
   )

   class Meta:
      ordering = ["id"]

   def __str__(self):
      return f"{self.product_name} X {self.quantity}"

