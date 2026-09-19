

from django.urls import path
from .views import (
   ProductListview
)

urlpatterns = [
    path("", 
         ProductListview.as_view(),
         name="product_list",
      ),
]
