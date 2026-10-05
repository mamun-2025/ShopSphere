
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from .forms import StockAdjustmentForm
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




# Inventory Stock Increase View
class InventoryStockIncreaseView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   FormView,
):
   form_class = StockAdjustmentForm
   template_name = "inventory/stock_adjustment.html"

   permission_required = "inventory.change_inventory"

   raise_exception = True



   def dispatch(self, request, *args, **kwargs):
       self.inventory = get_object_or_404(
          Inventory.objects.select_related("product"),
          pk=kwargs["pk"],
       )
       
       return super().dispatch(
          request, 
          *args, 
          **kwargs
      )


   def form_valid(self, form):
      quantity = form.cleaned_data["quantity"]

      self.inventory.increase_stock(quantity)
      
      messages.success(
         self.request,
         f"{quantity} stock added successfully",
      )

      return redirect(
         "inventory:detail",
         pk=self.inventory.pk,
      )




# Inventory Stock Decrease View
class InventoryStockDecreaseView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   FormView,
):
   form_class = StockAdjustmentForm
   template_name = "inventory/stock_adjustment.html"

   permission_required = "inventory.change_inventory"

   raise_exception = True


   def dispatch(self, request, *args, **kwargs):
      self.inventory = get_object_or_404(
         Inventory.objects.select_related("product"),
         pk=kwargs["pk"],
      )

      return super().dispatch(
         request, 
         *args, 
         **kwargs
      )


   def form_valid(self, form):
      quantity = form.cleaned_data["quantity"]

      try:
         self.inventory.decrease_stock(quantity)

      except ValueError as error:
         form.add_error(
            "quantity",
            str(error),
         )

         return self.form_invalid(form)


      messages.success(
         self.request,
         f"{quantity} stock removed successfully",
      )

      return redirect(
         "inventory:detail",
         pk=self.inventory.pk,
      )


      

   