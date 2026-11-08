
import requests

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from orders.models import Order
from payments.models import Payment
from payments.gateways.sslcommerz import create_payment_session

from django.conf import settings




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
         "Online payment is only available for pending orders."
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

   if method == Payment.Method.SSLCOMMERZ:
      if not (
         Decimal("10.00") <= order.total <= Decimal("500000.00")
      ):
         raise ValidationError(
            "SSLCommerz supports payment amounts"
            "between BDT 10 and BDT 500000."
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

   order.payment_method = method

   order.save(
      update_fields=[
         "payment_method",
         "updated_at",
      ]
   )

   return new_payment



# Create transaction ID Generator
def generate_transaction_id(payment):

   reference = payment.payment_reference.hex

   return f"SHOP-{reference[:25]}"



# Create Payment Payload 
def build_sslcommerz_payload(payment):

   order = payment.order
   user = payment.user 

   site_url = settings.SITE_URL.rstrip("/")

   tran_id = payment.gateway_transaction_id 

   payment_data = {
      "total_amount": str(payment.amount),
      "currency": payment.currency,
      "tran_id": tran_id,

      # Calback URLs
      "success_url": (
         f"{site_url}/payments/sslcommerz/success/"
      ),

      "fail_url": (
         f"{site_url}/payments/sslcommerz/fail/"
      ),

      "cancel_url": (
         f"{site_url}/payments/sslcommerz/cancel/"
      ),

      "ipn_url": (
         f"{site_url}/payments/sslcommerz/ipn/"
      ),

      # Customer Information
      "cus_name": order.shipping_full_name,
      "cus_email": order.email,
      "cus_phone": order.shipping_phone,

      "cus_add1": order.shipping_address_line,
      "cus_city": order.shipping_city_or_district,
      "cus_postcode": order.shipping_postal_code,
      "cus_country": "Bangladesh",

      # Product Information
      "product_name": f"ShopSphere Order {order.pk}",
      "product_category": "ecommerce",
      "product_profile": "physical-goods",

      # Shipping Information
      "shipping_method": "YES",
      "ship_name": order.shipping_full_name,
      "ship_add1": order.shipping_address_line,
      "ship_city": order.shipping_city_or_district,
      "ship_postcode": order.shipping_postal_code,
      "ship_country": "Bangladesh",

   }

   return payment_data




# Create SSLCommerz API Call
def start_sslcommerz_payment(*, order_id, user):

   # 1. Create Payment Attempt
   with transaction.atomic():

      payment = create_payment_attempt(
         order_id=order_id,
         user=user,
         method=Payment.Method.SSLCOMMERZ,
      )

      # Generate Unique transaction ID
      tran_id = generate_transaction_id(payment)

      # Save transaction ID before API request
      payment.gateway_transaction_id = tran_id

      payment.save(
         update_fields=[
            "gateway_transaction_id",
            "updated_at",
         ]
      )

   # 2. Reload Payment Information
   payment = (
      Payment.objects
      .select_for_update("order", "user")
      .get(
         pk=payment.pk,
      )
   )

   # 3. Build Gateway Payload
   payment_data = build_sslcommerz_payload(payment)

   # 4. Create Gateway Session
   try:
      result = create_payment_session(
         payment_data=payment_data,
      )
   except ValueError as exc:
      # Explicit gateway rejection or invalid response.
      # Do not classify an unknown network outcome here.

      Payment.objects.filter(
         pk=payment.pk,
         status=Payment.Status.PENDING,
      ).update(
         status=Payment.Status.FAILED,
      )
      raise ValidationError(str(exc))

   except requests.RequestException as exc:
      # Network error / timeout:
      # Gateway may already have created a session.
      # Keep the attempt pending for reconciliation.

      raise ValidationError(
         "payment gateway response is uncertain."
         "Please contact support before retrying."
      ) from exc 

   # 5. Save Gateway Session Information
   session_key = result.get("sessionkey")

   if not session_key:
      raise ValidationError(
         "Gateway session key was not returned."
         "Payment status requires reconciliation."
      )

   updated = Payment.objects.filter(
      pk=payment.pk,
      status=Payment.Status.PENDING,
   ).update(
      gateway_session_key=session_key,
   )

   if updated != 1:
      raise ValidationError(
         "Payment state changed unexpectedly."
      )

   # 6. Return Gateway url
   return {
      "payment": payment,
      "gateway_url": result["GatewayPageURL"],
   }




# Create Callback Identification Service
def indentify_sslcommerz_callback(*, callback_data):

   # 1. Get transaction ID
   tran_id = callback_data.get("tran_id")

   if not tran_id:
      raise ValidationError(
         "Transaction ID is missing."
      )

   # 2. Find Payment Attempt
   try:
      payment = (
         Payment.objects
         .select_for_update("order", "user")
         .get(
            gateway_transaction_id=tran_id,
            method=Payment.Method.SSLCOMMERZ,
         )
      )
   except Payment.DoesNotExist:
      raise ValidationError(
         "Payment transaction not found."
      )

   # 3. Check original currency if supplied
   currency = callback_data.get("currency_type")

   if currency and currency != payment.currency:
      raise ValidationError(
         "Transaction currency mismatch."
      )

   # 4. Check original amount if supplied
   amount = callback_data.get("currency_amount")

   if amount is not None:
      try:
         callback_amount = Decimal(str(amount))

      except (InvalidOperation, TypeError):
         raise ValidationError(
            "Invalid callback amount."
         )

      if callback_amount != payment.amount:
         raise ValidationError(
            "Transaction amount mismatch."
         )

   return payment
   