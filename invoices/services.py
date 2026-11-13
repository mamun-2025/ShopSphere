

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from orders.models import Order, OrderItem

from .models import Invoice, InvoiceItem, InvoiceNumberSequence


@transaction.atomic
def create_invoice_from_order(*, order):
   """
   Create one invoice from an existing order.

   Business Rules:
   1. One order = One invoice.
   2. Invoice number must be unique.
   3. Preserve order and item snapshots.
   4. Do not recalculate financial values.
   5. Create invoice and invoice items automically.
   """

   # 1. Lock the order 
   try:
      order = (
         Order.objects
         .select_for_update()
         .get(
            pk=order.pk
         )
      )

   except Order.DoesNotExist:
      raise ValidationError(
         "Order does not exist."
      )

   # 2. Prevent duplicate invoice creation.
   existing_invoice = Invoice.objects.filter(
      order=order
   ).first()


   if existing_invoice is not None:
      return existing_invoice

   # 3. Read order items
   order_items = list(
      OrderItem.objects.filter(
         order=order
      ).order_by("pk")
   )

   if not order_items:
      raise ValidationError(
         "Cannot create an invoice without order items."
      )

   # 4. Generate invoice number.
   year = timezone.localdate().year

   sequence, _ = InvoiceNumberSequence.objects.get_or_create(
      year=year,
      defaults={
         "last_number": 0,
      },
   )

   # Lock the sequence row.
   sequence = (
      InvoiceNumberSequence.objects
      .select_for_update()
      .get(
         pk=sequence.pk
      )
   )

   sequence.last_number += 1

   sequence.save(
      update_fields=["last_number"]
   )

   invoice_number = (
      f"INV--{year}--{sequence.last_number:06d}"
   )

   # 5. Create invoice snapshot.
   invoice = Invoice.objects.create(
      order=order,
      invoice_number=invoice_number,

      customer_name=order.shipping_full_name,
      customer_email=order.user.email or "",
      customer_phone=order.shipping_phone,

      shipping_address_line=order.shipping_address_line,
      shipping_area=order.shipping_area,
      shipping_city_or_district=order.shipping_city_or_district,
      shipping_postal_code=order.shipping_postal_code,
      shipping_zone_name=order.shipping_zone_name,
      shipping_method=order.shipping_method_name,

      payment_status=order.payment_status,
      payment_method=order.payment_method,

      subtotal=order.subtotal,
      tax_amount=order.tax_amount,
      shipping_fee=order.shipping_fee,
      service_fee=order.service_fee,

      coupon_code=order.coupon_code,
      discount_amount=order.discount_amount,

      total=order.total,

   )

   # 6. Create Invoice item snapshots.
   InvoiceItem.objects.bulk_create([
      InvoiceItem(
         invoice=invoice,

         product=item.product,
         product_name=item.product_name,

         unit_price=item.unit_price,
         quantity=item.quantiy,

         is_taxable=item.is_taxable,
         tax_rate=item.tax_rate,
         tax_amount=item.tax_amount,

         line_total=item.line_total,
      )
      for item in order_items
   ])

   return invoice



