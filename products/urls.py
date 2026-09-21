

from django.urls import path
from .views import (
   ProductListview,
   ProductDetailView,
   ProductCreateView,
   ProductUpdateView,
   ProductDeleteView
)

urlpatterns = [
   
   path("", 
         ProductListview.as_view(),
         name="product_list",
      ),
   path("create/",
           ProductCreateView.as_view(),
           name="product_create",
      ),
   path("<int:pk>/update/",
           ProductUpdateView.as_view(),
           name="product_update",
      ),
   path("<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
      ),
   path("<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
      ),
  
]
