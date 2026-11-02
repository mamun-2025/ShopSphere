

from .models import TaxRate
from decimal import Decimal, ROUND_HALF_UP


MONEY_PLACES = Decimal("0.01")
ZERO = Decimal("0.00")


def money(value):
   """Round a monetary value to two decimal places."""
   return Decimal(str(value)).quantize(
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


def calculate_items_totals(items):
   """
   Calculate totals from a list of objects containing:
   product and quantity.

   Tax is rounded per item, matching OrderItem calculation.
   """
 
   subtotal = ZERO
   taxable_subtotal = ZERO
   tax_amount = ZERO

   tax_rate_obj = get_default_tax_rate()

   if tax_rate_obj is not None:
      rate = Decimal(str(tax_rate_obj.rate))
      tax_name = tax_rate_obj.name 
   else:
      rate = ZERO
      tax_name = "No tax configured"


   for item in items:
      line_total = money(
         item.product.price * item.quantity
      )

      subtotal += line_total

      if item.product.is_taxable:
         taxable_subtotal += line_total

         line_tax = money(
            line_total * rate / Decimal("100")
         )

         tax_amount += line_tax

   subtotal = money(subtotal)
   taxable_subtotal = money(taxable_subtotal)
   tax_amount = money(tax_amount)

   total = money(subtotal + tax_amount)

   return {
      "subtotal": subtotal,
      "taxable_subtotal": taxable_subtotal,
      "tax_rate": rate,
      "tax_name": tax_name,
      "tax_amount": tax_amount,
      "total": total,
   }



def calculate_cart_totals(cart):
   items = list(
      cart.items.select_related("product").all()
   )

   return calculate_items_totals(items)