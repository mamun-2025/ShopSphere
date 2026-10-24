

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from categories.models import Category
from products.models import Product
from carts.models import Cart, CartItem
from taxes.models import TaxRate
from taxes.services import calculate_cart_totals, money 


User = get_user_model()


class TaxCalculationTests(TestCase):
   """
   Tests for ShopSphere's tax calculation service.
   Uses real Django database objects.
   """

   @classmethod
   def setUpTestData(cls):
      # 1. Create a test user
      cls.user = User.objects.create_user(
         username="tax_test_user",
         email="tax-test@example.com",
         password="test-password-123",
      )

      # 2. Create a product category
      cls.category = Category.objects.create(
         name="Tax_Test Category",
      )

      # 3. Create a taxable product
      cls.taxable_product = Product.objects.create(
         name="Taxable Product",
         slug="taxable-product",
         category=cls.category,
         sku="TAX-001",
         price=Decimal("500.00"),
         stock=20,
         is_active=True,
         is_taxable=True,
      )

      # 4. Create a non-taxable product
      cls.non_taxable_product = Product.objects.create(
         name="Non-Taxable Product",
         slug="non-taxable-product",
         category=cls.category,
         sku="TAX-002",
         price=Decimal("300.00"),
         stock=20,
         is_active=True,
         is_taxable=False,
      )

      # 5. Create the user's cart
      cls.cart  = Cart.objects.create(user=cls.user)

   def setUp(self):
      TaxRate.objects.all().delete()

      self.cart.items.all().delete()

      CartItem.objects.create(
         cart=self.cart,
         product=self.taxable_product,
         quantity=2,
      )

      CartItem.objects.create(
         cart=self.cart,
         product=self.non_taxable_product,
         quantity=1,
      )

   def create_tax_rate(
         self,
         rate="5.00",
         is_active=True,
         is_default=True,
   ):
      return TaxRate.objects.create(
         name="Test Tax",
         rate=Decimal(rate),
         is_active=is_active,
         is_default=is_default,
      )


   def test_calculates_tax_and_total_correctly(self):
      self.create_tax_rate(rate="5.00")

      result = calculate_cart_totals(self.cart)

      # 500 X 2 + 300 X 1 = 1300
      self.assertEqual(
         result["subtotal"],
         Decimal("1300.00"),
      )

      # Only the taxable product is included; 500 X 2 = 1000
      self.assertEqual(
         result["taxable_subtotal"],
         Decimal("1000.00"),
      )

      # 1000 X 5 / 100 = 50
      self.assertEqual(
         result["tax_amount"],
         Decimal("50.00"),
      )

      # 1300 + 50 = 1350
      self.assertEqual(
         result["tax_rate"],
         Decimal("5.00"),
      )

      self.assertEqual(
         result["tax_name"],
         "Test Tax",
      )

   def test_non_taxable_product_is_excluded_from_tax(self):
      self.create_tax_rate(rate="10.00")

      result = calculate_cart_totals(self.cart)

      self.assertEqual(
         result["taxable_subtotal"],
         Decimal("1000.00"),
      )

      self.assertEqual(
         result["tax_amount"],
         Decimal("100.00"),
      )

      self.assertEqual(
         result["total"],
         Decimal("1400.00"),
      )

   def test_inactive_tax_rate_is_not_used(self):
      self.create_tax_rate(
         rate="5.00",
         is_active=False,
         is_default=True,
      )

      result = calculate_cart_totals(self.cart)

      self.assertEqual(
         result["tax_rate"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["tax_amount"],
         Decimal("0.00"),
      )

      self.assertEqual(
        result["total"],
        Decimal("1300.00"),
      )

      self.assertEqual(
         result["tax_name"],
         "No tax configured",
      )

   def test_no_tax_rate_returns_zero_tax(self):
      result = calculate_cart_totals(self.cart)

      self.assertEqual(
         result["tax_rate"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["tax_amount"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["total"],
         Decimal("1300.00"),
      )

   def test_money_rounds_to_two_decimal_places(self):
      self.assertEqual(
         money(Decimal("1.005")),
         Decimal("1.01"),
      )

      self.assertEqual(
         money(Decimal("1.004")),
         Decimal("1.00"),
      )

   def test_tax_calculation_rounds_correctly(self):
      self.cart.items.all().delete()

      rounding_product = Product.objects.create(
         name="Rounding Test Product",
         slug="rounding-test-product",
         category=self.category,
         sku="TAX-003",
         price=Decimal("10.05"),
         stock=10,
         is_active=True,
         is_taxable=True,
      )

      CartItem.objects.create(
         cart=self.cart,
         product=rounding_product,
         quantity=1,
      )

      self.create_tax_rate(rate="10.00")

      result = calculate_cart_totals(self.cart)

      self.assertEqual(
         result["subtotal"],
         Decimal("10.05"),
      )

      self.assertEqual(
         result["tax_amount"],
         Decimal("1.01"),
      )

      self.assertEqual(
         result["total"],
         Decimal("11.06"),
      )

   def test_invalid_tax_rate_above_100_is_rejected(self):
      tax_rate = TaxRate(
         name="Invalid Tax",
         rate=Decimal("100.01"),
         is_active=True,
         is_default=True,
      )

      with self.assertRaises(ValidationError):
         tax_rate.full_clean()


   def test_nagative_tax_rate_is_rejected(self):
      tax_rate = TaxRate(
         name="Nagative Tax",
         rate=Decimal("-1.00"),
         is_active=True,
         is_default=True,
      )

      with self.assertRaises(ValidationError):
         tax_rate.full_clean()


   def test_empty_cart_has_zero_total(self):
      self.cart.items.all().delete()
      self.create_tax_rate(rate="5.00")

      result = calculate_cart_totals(self.cart)

      self.assertEqual(
         result["subtotal"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["taxable_subtotal"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["tax_amount"],
         Decimal("0.00"),
      )

      self.assertEqual(
         result["total"],
         Decimal("0.00"),
      )
    
