

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView

from weasyprint import HTML

from .models import Invoice


class InvoiceDetailView(LoginRequiredMixin, DetailView):

    model = Invoice
    template_name = "invoices/invoice_detail.html"
    context_object_name = "invoice"

    slug_field = "invoice_number"
    slug_url_kwarg = "invoice_number"

    def get_queryset(self):
        return (
            Invoice.objects
            .filter(order__user=self.request.user)
            .select_related("order")
            .prefetch_related("items")
        )


class InvoicePDFView(LoginRequiredMixin, DetailView):

    model = Invoice

    slug_field = "invoice_number"
    slug_url_kwarg = "invoice_number"

    def get_queryset(self):
        return (
            Invoice.objects
            .filter(order__user=self.request.user)
            .select_related("order")
            .prefetch_related("items")
        )

    def render_to_response(self, context, **response_kwargs):

        invoice = context["object"]

        html_string = render_to_string(
            "invoices/invoice_pdf.html",
            {
                "invoice": invoice,
            },
            request=self.request,
        )

        pdf_file = HTML(
            string=html_string,
            base_url=self.request.build_absolute_uri("/"),
        ).write_pdf()

        response = HttpResponse(
            pdf_file,
            content_type="application/pdf",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="{invoice.invoice_number}.pdf"'
        )

        return response
