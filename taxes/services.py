

from .models import TaxRate
from decimal import Decimal, ROUND_HALF_UP


MONEY_PLACES = Decimal("0.01")
ZERO = Decimal("0.00")


def money(value):
   """Round a monetary value to two decimal places."""
   return Decimal(value).quantize(
      MONEY_PLACES,
      rounding=ROUND_HALF_UP,
   )


def get_default_tax_rate():
   """Return the active default tax rate, if configured."""
   return (
      TaxRate.objects.
      filter(is_active=True, is_default=True)
      .order_by("-updated_at")
      .first()
   )


def calculate_cart_totals(cart):
   """
   Calculate cart subtotal, taxable subtotal, tax, and total.

   Tax is calculated only on active cart lines' taxable products.
   Product availability and stock validation remain separate concerns.
   """
   cart_items = cart.items.select_related("product").all()

   subtotal = ZERO
   taxable_subtotal = ZERO

   for item in cart_items:
      line_total = item.product.price * item.quantity 
      subtotal += line_total

      if item.product.is_taxable:
         taxable_subtotal += line_total

      subtotal = money(subtotal)
      taxable_subtotal = money(taxable_subtotal)

      tax_rate_obj = get_default_tax_rate()

      if tax_rate_obj is not None:
         rate = tax_rate_obj.rate
         tax_amount = money(
            taxable_subtotal * rate / Decimal("100")
         )
         tax_name = tax_rate_obj.name 

      else:
         rate = ZERO
         tax_amount = ZERO
         tax_name = "No tax configured"

      total = money(subtotal + tax_amount)

      return {
         "subtotal": subtotal,
         "taxable_subtotal": taxable_subtotal,
         "tax_rate": rate,
         "tax_name": tax_name,
         "tax_amount": tax_amount,
         "total": total,
      }
