
from django.core.exceptions import ValidationError
from django.db import transaction

from orders.models import Order
from payments.models import Payment


ONLINE_PAYMENT_METHODS = {
   Payment.Method.SSLCOMMERZ,
   Payment.Method.BKASH,
   Payment.Method.NAGAD,
}

ACTIVE_PAYMENT_STATUSES = {
   Payment.Status.PENDING,
   Payment.Status.PROCESSING,
}


@transaction.atomic
def create_payment_attempt(
   *,
   order_id,
   user, 
   method,
):
   # 1.Locck the Customer's order
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

   # 2. Validate Payment Method
   if method not in ONLINE_PAYMENT_METHODS:
      raise ValidationError(
         "Unsupported online payment method."
      )

   # 3. Only pending orders can start online payment
   if order.status != Order.Status.PENDING:
      raise ValidationError(
         "Online payment is only available for pedning orders."
      )

   # 4. Prevent duplicate successful payment
   if order.payment_status == Order.PaymentStatus.PAID:
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

   # 5. Prevent multiple active attempts
   active_payment = order.payments.filter(
      status__in=ACTIVE_PAYMENT_STATUSES
   ).exists()

   if active_payment:
      raise ValidationError(
         "An active payment attempt already exists."
      )

   # 6. Validate amount
   if order.total is None or order.total <= 0:
      raise ValidationError(
         "Invalid order amount."
      )

   # 7. Create payment attempt
   new_payment = Payment.objects.create(
      order=order,
      user=user,
      amount=order.total,
      currency="BDT",
      method=method,
      status=Payment.Status.PENDING,
   )

   return new_payment


