
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .forms import StockAdjustmentForm
from .models import Inventory



# Inventory List View
class InventoryListView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   ListView,
):
   model = Inventory
   template_name = "inventory/inventory_list.html"
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




# Common Stock Adjustment View
class InventoryStockAdjustmentBaseView(
   LoginRequiredMixin,
   PermissionRequiredMixin,
   FormView,
):
   form_class = StockAdjustmentForm
   template_name = "inventory/stock_adjustment.html"

   permission_required = "inventory.adjust_stock"

   raise_exception = True


   def get_inventory(self):
      if not hasattr(self, "inventory"):
         self.inventory = get_object_or_404(
            Inventory.objects.select_related("product"),
            pk=self.kwargs["pk"],
         )

         return self.inventory
      
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["inventory"] = self.get_inventory()
      return context

   def form_valid(self, form):
      
      inventory = self.get_inventory()
      quantity = form.cleaned_data["quantity"]

      try:
         self.adjust_stock(inventory, quantity)

      except ValidationError as error:
         form.add_error("quantity", error)
         return self.form_invalid(form)
      
      messages.success(
         self.request,
         self.get_success_message(quantity),
      )

      return redirect(
         "inventory:detail",
         pk=inventory.pk,
      )

   def adjust_stock(self, inventory, quantity):
      raise NotImplementedError(
         "Subclasses must implement ajust_stock()."
      )

   def get_success_message(self, quantity):
      raise NotImplementedError(
         "Subclasses must implement get_success_message()."
      )


# Inventory Stock Increase View
class InventoryStockIncreaseView(
   InventoryStockAdjustmentBaseView,
):
   def adjust_stock(self, inventory, quantity):
      inventory.increase_stock(quantity)

   def get_success_message(self, quantity):
      return f"{quantity} stock added successfully."





# Inventory Stock Decrease View
class InventoryStockDecreaseView(
   InventoryStockAdjustmentBaseView,
):
   def adjust_stock(self, inventory, quantity):
      inventory.decrease_stock(quantity)

   def get_success_message(self, quantity):
      return f"{quantity} stock removed successfully."

      

   