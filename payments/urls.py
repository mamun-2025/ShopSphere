

from django.urls import path 

from payments import views

app_name = "payments"


urlpatterns = [
    path(
       "sslcommerz/start/<int:order_id>/",
       views.sslcommerz_payment_start,
       name="sslcommerz_start",
    ),
    
]
