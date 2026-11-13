

from django.urls import path 

from . import views

app_name = "invoices"


urlpatterns = [
    path(
       "<str:invoice_number>/",
       views.InvoiceDetailView.as_view(),
       name="detail",
    ),
    path(
       "<str:invoice_number>/pdf/",
       views.InvoicePDFView.as_view(),
       name="pdf",
    ),

]
