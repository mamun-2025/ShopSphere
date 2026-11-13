
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from . models import Invoice


class InvoiceDetailView(LoginRequiredMixin, DetailView):

   model = Invoice

   template_name = "invoices/invoice_detail.html"

   context_object_name = "invoice"

   slug_field = "invoice_number"
   slug_url_kwarg = "invoice_number"

   def get_queryset(self):
      return (
         Invoice.objects
         .filter(
            order__user=self.request.user 
         )
         .select_related(
            "order",
         )
         .prefetch_related(
            "items",
         )
      )

