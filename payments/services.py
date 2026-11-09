
import requests

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from orders.models import Order
from payments.models import Payment
from payments.gateways.sslcommerz import create_payment_session, validate_sslcommerz_transaction

from django.conf import settings

from django.urls import reverse




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

   def callback_url(name):
      path = reverse(f"payments:{name}")
      return f"{site_url}{path}"

   payment_data = {
      "total_amount": str(payment.amount),
      "currency": payment.currency,
      "tran_id": payment.gateway_transaction_id,

      # Calback URLs
      "success_url": callback_url(
         "sslcommerz_success"
      ),

      "fail_url": callback_url(
         "sslcommerz_fail"
      ),

      "cancel_url": callback_url(
         "sslcommerz_cancel"
      ),

      "ipn_url": callback_url(
         "sslcommerz_ipn"
      ),
      

      # Customer Information
      "cus_name": order.shipping_full_name,
      "cus_email": user.email,
      "cus_phone": order.shipping_phone,

      "cus_addl": order.shipping_address_line,
      "cus_city": order.shipping_city_or_district,
      "cus_postcode": order.shipping_postal_code,
      "cus_country": "Bangladesh",

      # Product Information
      "product_name": f"ShopSphere Order {order.pk}",
      "product_category": "ecommerce",
      "product_profile": "physical-goods",

      # Shipping Information
      "shipping_method": "YES",
      "num_of_item": sum(
         item.quantity for item in order.items.all()
      ),

      "ship_name": order.shipping_full_name,
      "ship_addl": order.shipping_address_line,
      "ship_area": order.shipping_area,
      "ship_city": order.shipping_city_or_district,
      "ship_postcode": order.shipping_postal_code or "0000",
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
      .select_related("order", "user")
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

      # Only mark FAILED when the gateway
      # explicitly rejects the request.
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

   payment.refresh_from_db()

   # 6. Return Gateway url
   return {
      "payment": payment,
      "gateway_url": result["GatewayPageURL"],
   }




# Create Callback Identification Service
def identify_sslcommerz_callback(*, callback_data):

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
         .select_related("order", "user")
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

   if currency != payment.currency:
      raise ValidationError(
         "Transaction currency mismatch."
      )


   # 4. Check original amount if supplied
   amount = callback_data.get("currency_amount")

   if not amount:
      raise ValidationError("Callback amount is missing.")

   try:
      callback_amount = Decimal(str(amount))

   except (InvalidOperation, TypeError):
      raise ValidationError("Invalid callback amount.")

   if callback_amount != payment.amount:
      raise ValidationError(
         "Transaction amount mismatch."
      )

   return payment




# Verify SSLCommerz Payment
def verify_sslcommerz_payment(*, tran_id, val_id):

   # 1. Find our Payment
   try:
      payment = Payment.objects.get(
         gateway_transaction_id=tran_id,
         method=Payment.Method.SSLCOMMERZ,
      )

   except Payment.DoesNotExist:
      raise ValidationError("Payment not found.")

   # 2. Call SSLCommerz Validation API
   result = validate_sslcommerz_transaction(
      val_id=val_id,
   )

   # 3. Validate gateway status
   if result.get("status") not in {"VALID", "VALIDATED"}:
      raise ValidationError(
         "SSLCommerz transaction is not valid."
      )

   # 4. Match transaction ID
   if result.get("tran_id") != payment.gateway_transaction_id:
      raise ValidationError(
         "Transaction ID mismatch."
      )

   # 5. Match validation ID
   if result.get("val_id") != val_id:
      raise ValidationError(
         "Validation Id mismatch."
      )

   # 6. Match currency
   if result.get("currency_type") != payment.currency:
      raise ValidationError(
         "Payment currency mismatch."
      )

   # 7. Match original amount
   try:
      verified_amount = Decimal(
         str(result["currency_amount"])
      )

   except (KeyError, InvalidOperation, TypeError):
      raise ValidationError(
         "Invalid verified payment amount."
      )

   if (
      not verified_amount.is_finite()
      or verified_amount != payment.amount
   ):
      raise ValidationError(
         "Payment amount mismatch."
      )

   # 8. Validate risk level 
   try:
      risk_level = int(result.get("risk_level", -1))

   except (ValueError, TypeError):
      raise ValidationError(
         "Invalid payment risk level."
      )

   if risk_level not in (0, 1):
      raise ValidationError(
         "Unknown payment risk level."
      )

   # 9. Lock Order first, then Payment.
   # Gateway network request has already completed.
   with transaction.atomic():

      order = (
         Order.objects
         .select_for_update()
         .get(
            pk=payment.order_id
         )
      )

      locked_payment = (
         Payment.objects
         .select_for_update()
         .get(
            pk=payment.pk
         )
      )

      # 10. Idempotency
      # Already successful? Return without updating again.
      if locked_payment.status == Payment.Status.SUCCESS:

         if (
            locked_payment.gateway_validation_id == val_id
            and order.payment_status == Order.PaymentStatus.PAID
         ):
            return locked_payment

         raise ValidationError(
            "Payment is already completed."
         )

      # 11. Only active payments can be verified.
      if locked_payment.status not in ACTIVE_PAYMENT_STATUSES:
         raise ValidationError(
            "Payment is not in an active state."
         )
   

      # 12. Prevent another successful payment 
      other_success = (
         order.payments 
         .filter(status=Payment.Status.SUCCESS)
         .exclude(
            pk=locked_payment.pk
         ).exists()
      )

      if other_success or order.payment_status == Order.PaymentStatus.PAID:
         raise ValidationError(
            "Another payment has already paid this order."
         )

      # 13. Save gateway verification information
      locked_payment.gateway_validation_id = val_id

      locked_payment.gateway_bank_transaction_id = (
         result.get("bank_tran_id") or ""
      )

      locked_payment.gateway_risk_level = risk_level

      # 14. Risky payment: do not fulfil automatically 
      if risk_level == 1:
         
         locked_payment.status = Payment.Status.PROCESSING

         locked_payment.save(
            update_fields=[
               "gateway_validation_id",
               "gateway_bank_transaction_id",
               "gateway_risk_level",
               "status",
               "updated_at",
            ]
         )

         return locked_payment

      # 15. Save and verified payment 
      locked_payment.status = Payment.Status.SUCCESS

      locked_payment.save(
         update_fields=[
            "gateway_validation_id",
            "gateway_bank_transaction_id",
            "gateway_risk_level",
            "status",
            "updated_at",
         ]
      )

      # 16. Update Order Payment status
      order.payment_status = Order.PaymentStatus.PAID

      order.save(
         update_fields=[
            "payment_status",
            "updated_at",
         ]
      )

      return locked_payment





