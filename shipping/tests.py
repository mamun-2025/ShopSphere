
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from taxes.services import calculate_cart_totals


class CalculateCartTotalsTests(SimpleTestCase):
   def setUp(self):
      taxable_item = SimpleNamespace(
         product=SimpleNamespace(
            price=Decimal("500.00"),
            is_taxable=True,
         ),
         quantity=2,
      )

      non_taxable_item = SimpleNamespace(
         product=SimpleNamespace(
            price=Decimal("300.00"),
            is_taxable=False,
         ),
         quantity=1,
      )

      self.cart = MagicMock()
      self.cart.items.select_related.return_value.all.return_value = [
         taxable_item,
         non_taxable_item,
      ]


   @patch("taxes.services.get_default_tax_rate")
   def test_calculates_tax_correctly(self, mock_tax_rate):
      mock_tax_rate.return_value = SimpleNamespace(
         name="Test Tax",
         rate=Decimal("5.00"),
      )

      result = calculate_cart_totals(self.cart)

      self.assertEqual(result["subtotal"], Decimal("1300.00"))
      self.assertEqual(result["taxable_subtotal"], Decimal("1000.00"))

      self.assertEqual(result["tax_amount"], Decimal("50.00"))
      self.assertEqual(result["total"], Decimal("1350.00"))

   @patch("taxes.services.get_default_tax_rate")
   def test_no_configured_tax_means_zero_tax(self, mock_tax_rate):
      mock_tax_rate.return_value = None

      result = calculate_cart_totals(self.cart)

      self.assertEqual(result["tax_rate"], Decimal("0.00"))
      self.assertEqual(result["tax_amount"], Decimal("0.00"))
      self.assertEqual(result["total"], Decimal("1300.00"))

