

from .models import Category
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
   ListView,
   CreateView,
   UpdateView,
   DeleteView,
)

class CategoryListView(ListView):
   model = Category
   template_name = "categories/category_list.html"
   context_object_name = "categories"

   def get_queryset(self):
      return Category.objects.filter(is_active=True)


class CategoryCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
   model = Category
   form_class = CategoryForm
   template_name = "categories/category_form.html"
   success_url = reverse_lazy("category_list")
   permission_required = "categories.add_category"


class CategoryUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
   model = Category
   form_class = CategoryForm
   template_name = "categories/category_form.html"
   success_url = reverse_lazy("category_list")
   permission_required = "categories.change_category"


class CategoryDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
   model = Category
   template_name = "categories/category_confirm_delete.html"
   success_url = reverse_lazy("category_list")
   permission_required = "categories.delete_category"

