

from django.urls import path 
from .views import ReviewCreateView

app_name = "reviews"

urlpatterns = [
   path(
      "product/<int:product_id>/create/",
      ReviewCreateView.as_view(),
      name="review_create",
   ),
]
