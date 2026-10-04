

from django.urls import path 
from . import views

app_name = "inventory"

urlpatterns = [
    path(
       "",
       views.InventoryListView.as_view(),
       name="list",
    ),
    path(
       "<int:pk>",
       views.InventoryDetailView.as_view(),
       name="detail",
    ),

]
