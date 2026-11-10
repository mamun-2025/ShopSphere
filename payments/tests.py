
import requests
from decimal import Decimal
from unittest.mock import patch

from django.test import RequestFactory
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from orders.models import Order
from payments.models import Payment
from payments.services import (
   create_payment_attempt,
   verify_sslcommerz_payment,
   start_sslcommerz_payment,
   identify_sslcommerz_callback,
)
from payments.views import sslcommerz_cancel, sslcommerz_fail

User = get_user_model()


class PaymentIdempotencyTests(TestCase):

   def setUp(self):
      self.user = User.objects.create(
            username="Payment_test_user",
            email="payment@example.com",
            password="TestPassword123!",
         )
      
      self.order = Order.objects.create(
            user=self.user,
            status=Order.Status.PENDING,
            payment_method=Order.PaymentMethod.SSLCOMMERZ,
            payment_status=Order.PaymentStatus.UNPAID,
            subtotal=Decimal("700.00"),
            tax_amount=Decimal("20.00"),
            shipping_fee=Decimal("70.00"),
            service_fee=Decimal("0.00"),
            total=Decimal("770.00"),
         )
      
   def test_order_is_created(self):
      self.assertEqual(self.order.user, self.user)
      self.assertEqual(self.order.total, Decimal("770.00"))
      self.assertEqual(
         self.order.payment_status,
         Order.PaymentStatus.UNPAID,
      )



   def test_cannot_create_duplicate_active_payment(self):
      first_payment = create_payment_attempt(
         order_id=self.order.pk,
         user=self.user,
         method=Payment.Method.SSLCOMMERZ,
      )

      with self.assertRaises(ValidationError):
         create_payment_attempt(
            order_id=self.order.pk,
            user=self.user,
            method=Payment.Method.SSLCOMMERZ,
         )

      self.assertEqual(
         Payment.objects.filter(
            order=self.order
         ).count(),
         1,
      )



   def test_duplicate_gateway_transaction_id_is_rejected(self):
      Payment.objects.create(
         order=self.order,
         user=self.user,
         amount=Decimal("770.00"),
         currency="BDT",
         method=Payment.Method.SSLCOMMERZ,
         status=Payment.Status.PENDING,
         gateway_transaction_id="SHOP-TEST-123",
      )

      with self.assertRaises(IntegrityError):
         with transaction.atomic():
            Payment.objects.create(
               order=self.order,
               user=self.user,
               amount=Decimal("770.00"),
               currency="BDT",
               method=Payment.Method.SSLCOMMERZ,
               status=Payment.Status.PENDING,
               gateway_transaction_id="SHOP-TEST-123",
            )



   def test_duplicate_success_callback_is_idempotent(self):
      payment = Payment.objects.create(
         order=self.order,
         user=self.user,
         amount=Decimal("770.00"),
         currency="BDT",
         method=Payment.Method.SSLCOMMERZ,
         status=Payment.Status.PENDING,
         gateway_transaction_id="SHOP-TEST-123",
      )

      gateway_response = {
         "status": "VALID",
         "tran_id": "SHOP-TEST-123",
         "val_id": "VAL-TEST-456",
         "currency_type": "BDT",
         "currency_amount": "770.00",
         "risk_level": 0,
         "bank_tran_id": "BANK-TEST-456",
      }

      with patch(
         "payments.services.validate_sslcommerz_transaction",
         return_value=gateway_response,
      ) as mock_validate:

         # First Callback
         first_result = verify_sslcommerz_payment(
            tran_id="SHOP-TEST-123",
            val_id="VAL-TEST-456",
         )

         # Duplicate callback
         second_result = verify_sslcommerz_payment(
            tran_id="SHOP-TEST-123",
            val_id="VAL-TEST-456",
         )

         # Both calls return the same Payment record.
         self.assertEqual(first_result.pk, payment.pk)
         self.assertEqual(second_result.pk, payment.pk)

         # Payment must remain SUCCESS.
         self.assertEqual(
            second_result.status,
            Payment.Status.SUCCESS,
         )

         # Order must remain PAID
         self.order.refresh_from_db()

         self.assertEqual(
            self.order.payment_status,
            Order.PaymentStatus.PAID,
         )

         # No duplicate Payment record.
         self.assertEqual(
            Payment.objects.filter(order=self.order).count(),
            1,
         )

         # Gateway validation is called for both callbacks.
         self.assertEqual(
            mock_validate.call_count,
            2,
         )


   def test_failed_payment_allows_new_attempt(self):
      failed_payment = Payment.objects.create(
         order=self.order,
         user=self.user,
         amount=Decimal("770.00"),
         currency="BDT",
         method=Payment.Method.SSLCOMMERZ,
         status=Payment.Status.FAILED,
         gateway_transaction_id="SHOP-FAILED-001",
      )

      new_payment = create_payment_attempt(
         order_id=self.order.pk,
         user=self.user,
         method=Payment.Method.SSLCOMMERZ,
      )

      self.assertEqual(
         new_payment.status,
         Payment.Status.PENDING,
      )

      self.assertNotEqual(
         new_payment.pk,
         failed_payment.pk,
      )

      self.assertEqual(
         Payment.objects.filter(
            order=self.order
         ).count(),
         2,
      )



   def test_gateway_timeout_keeps_payment_pending(self):
      with patch(
         "payments.services.create_payment_session",
         side_effect=requests.Timeout("Gateway timeout"),
      ):
         with self.assertRaises(ValidationError):
            start_sslcommerz_payment(
               order_id=self.order.pk,
               user=self.user,
            )

      payment = Payment.objects.get(order=self.order)

      self.assertEqual(
         payment.status,
         Payment.Status.PENDING,
      )

      self.assertTrue(
         payment.gateway_transaction_id
      )

      self.assertEqual(
         Payment.objects.filter(
            order=self.order
         ).count(),
         1,
      )



   def test_gateway_rejection_marks_payment_failed(self):
      with patch(
         "payments.services.create_payment_session",
         side_effect=ValueError("Gateway rejected payment request."),
      ):
         with self.assertRaises(ValidationError):
            start_sslcommerz_payment(
               order_id=self.order.pk,
               user=self.user,
            )

         payment = Payment.objects.get(order=self.order)

         self.assertEqual(
            payment.status,
            Payment.Status.FAILED,
         )

         self.assertTrue(
            payment.gateway_transaction_id
         )

         self.assertEqual(
            Payment.objects.filter(
               order=self.order
            ).count(),
            1,
         )


   def test_cancel_callback_does_not_change_payment_status(self):
      payment = Payment.objects.create(
         order=self.order,
         user=self.user,
         amount=Decimal("770.00"),
         currency="BDT",
         method=Payment.Method.SSLCOMMERZ,
         status=Payment.Status.PENDING,
         gateway_transaction_id="SHOP-CANCEL-001",
      )

      factory = RequestFactory()

      request = factory.post(
         "/payments/sslcommerz/cancel",
         {
            "tran_id": "SHOP-CANCEL-001",
            "currency_type": "BDT",
            "currency_amount": "770.00",
         },
      )

      response = sslcommerz_cancel(request)

      self.assertEqual(
         response.status_code,
         200,
      )

      payment.refresh_from_db()

      self.assertEqual(
         payment.status,
         Payment.Status.PENDING,
      )



   def test_invalid_callback_transaction_is_rejected(self):
      callback_data = {
         "tran_id": "INVALID-TRANSACTION-999",
         "currency_type": "BDT",
         "currency_amount": "770.00",
      }

      with self.assertRaises(ValidationError):
         identify_sslcommerz_callback(
            callback_data=callback_data,
         )



   def test_fail_callback_does_not_change_payment_status(self):
      payment = Payment.objects.create(
         order=self.order,
         user=self.user,
         amount=Decimal("770.00"),
         currency="BDT",
         method=Payment.Method.SSLCOMMERZ,
         status=Payment.Status.PENDING,
         gateway_transaction_id="SHOP-FAIL-001",
      )

      factory = RequestFactory()

      request = factory.post(
         "/payments/sslcommerz/fail/",
         {
            "tran_id": "SHOP-FAIL-001",
            "currency_type": "BDT",
            "currency_amount": "770.00",
         },
      )

      response = sslcommerz_fail(request)

      self.assertEqual(
         response.status_code,
         200,
      )

      payment.refresh_from_db()

      self.assertEqual(
         payment.status,
         Payment.Status.PENDING,
      )
