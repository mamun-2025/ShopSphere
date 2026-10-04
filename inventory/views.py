
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Inventory


# Inventory List View
class InventoryListView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   ListView,
):
   model = Inventory
   template_name = "inventory/Inventory_list.html"
   context_object_name = "inventories"

   permission_required = "inventory.view_inventory"

   raise_exception = True


   def get_queryset(self):
      return (
         Inventory.objects
         .select_related("product")
         .order_by("product__name")
      )



# Inventory DetailView
class InventoryDetailView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   DetailView,
):
   model = Inventory
   template_name = "inventory/inventory_detail.html"
   context_object_name = "inventory"

   permission_required = "inventory.view_inventory"

   raise_exception = True


   def get_queryset(self):
      return Inventory.objects.select_related(
         "product"
      )