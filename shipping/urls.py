

from django.urls import path
from .views import ShippingOptionsView

app_name = "shipping"

urlpatterns = [
    path(
       "options/",
       ShippingOptionsView.as_view(),
       name="options",
    ),
]
