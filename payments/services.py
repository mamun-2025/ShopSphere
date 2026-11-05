
from django.core.exceptions import ValidationError
from django.db import transaction

from orders.models import Order
from payments.models import Payment


@transaction.atomic
def create_payment_attempt(
   *,
   order_id,
   user, 
   method,
):
   # Locck the Order row
   try:
      order = (
         Order.objects
         .select_for_update()
         .get(
            pk=order_id,
            user=user,
         )
      )

   except Order.DoesNotExist:
      raise ValidationError(
         "Order not found or you do not have permission."
      )

   # 2. Check supported online payment methods
   allowed_methods = [
      Payment.Method.SSLCOMMERZ,
      Payment.Method.BKASH,
      Payment.Method.NAGAD,
   ]
 
   if method not in allowed_methods:
      raise ValidationError(
         "Unsupported online payment method."
      )

   # 3. Prevent payment for cancelled orders
   if order.status == "cancelled":
      raise ValidationError(
         "Cannot pay for a cancelled order."
      )

   if order.payment_status == "paid":
      raise ValidationError(
         "This order has already been paid."
      )

   successful_payment = order.payments.filter(
      status=Payment.Status.SUCCESS
   ).exists()

   if successful_payment:
      raise ValidationError(
         "This order has already been paid."
      )

   active_payment = order.payments.filter(
      status__in=[
         Payment.Status.PENDING,
         Payment.Status.PROCESSING,
      ]
   ).exists()

   if active_payment:
      raise ValidationError(
         "An active payment attempt already exists."
      )

   if order.total is None or order.total <= 0:
      raise ValidationError(
         "Invalid order amount."
      )

   new_payment = Payment.objects.create(
      order=order,
      user=user,
      amount=order.total,
      currency="BDT",
      method=method,
      status=Payment.Status.PENDING,
   )

   return new_payment


