
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages


class ProductListview(ListView):
   model = Product
   template_name = "products/product_list.html"
   context_object_name = "products"

   def get_queryset(self):
      return Product.objects.filter(
         is_active=True
      )

"""
1. What is ListView?
= ListView is a Django generic class-based view used to display a list of objects from a model.
2. What does get_queryset() do>
= get_queryset() allows us to customize which objects are returned by a class-based view.
3. Why use context_object_name?
= It allows us to define a meaningful name for the objects passed to the template.
4. What is a QuerySet?
= A QuerySet is a collection of database queries representing objects retrieved from a Django model.

"""

class ProductDetailView(DetailView):
   model = Product
   template_name = "products/product_detail.html"
   context_object_name = "product"

   def get_queryset(self):
      return Product.objects.filter(
         is_active=True
      )


"""

1. What is Django DetailView?
= DetailView is a Django generic class-based view used to display the details of a single model object.
2. What is pk?
= pk stands for Primary Key. It is used to uniquely identify a database record.
3. What does <int:pk> meand?
= It captures an integer value from the URL and passes it to the view as pk.
Example:
   /products/10/
   pk = 10

"""


class ProductCreateView(LoginRequiredMixin, CreateView):
   model = Product
   form_class = ProductForm
   template_name = "products/product_form.html"
   success_url = reverse_lazy("product_list")
   

   def form_valid(self, form):

      messages.success(
         self.request,
         "Product create successfully"
      )

      return super().form_valid(form)
   


"""

1. What is CreateView?
= CreateView is a Django generic class-based view used used to create a new model object through a form.
2. Why is ModelForm?
= A ModelForm automatically creates form fields and validation based on a Django model.
3. Why use LoginRequiredMixin?
= It ensures that only authenticated users can access the view.
4. Why is reverse_lazy()?
= It resolves a URL by its URL name and is commonly used for class-based view configuration such as success_url.
5. Why use POST for creating a product?
= Because creating a product changes server-side data and creates a new database record.

"""



class ProductUpdateView(LoginRequiredMixin, UpdateView):
   model = Product
   form_class = ProductForm
   template_name = "products/product_form.html"
   context_object_name = "product"
   success_url = reverse_lazy("product_list")


   def form_valid(self, form):

      messages.success(
         self.request,
         "Product updated successfully"
      )

      return super().form_valid(form)



"""
1. What is UpdateView?
= Updateview is a Django generic class-based view used to update an existing model object through a form.
2. Can we use the same ModelForm for CreateView and UpdateView?
= Yes, ProductForm used for both CreateView and UpdateView.
3. How does UpdateView know which object to update?
= UpdateView Finds existing object from URL with primary key(<int:pk>).
4. Does UpdateView create a new object?
= No, It's update existing object.
5. What is instance?
= instance specifies the existing model object that a ModelForm should edit.

"""


class ProductDeleteView(LoginRequiredMixin, DeleteView):
   model = Product
   template_name = "products/product_confirm_delete.html"
   context_object_name = "product"
   success_url = reverse_lazy("product_list")

   def form_valid(self, form):

      messages.success(
         self.request,
         "Product delete succssfully"
      )

      return super().form_valid(form)


"""
1. What is DeleteView?
= DeleteView is a Django generic class-based view used to delete an existing model obejct.
2. Why use a confirmation page?
= To prevent accidental deletion and allow the user to confirm the destructive action.
3. Why use POST for deletion?
= Deletion changes server-side data, so it should not be performed through a normal GET request.
4. What does pk do?
= It defines the specific object that should be deleted.
5. What happens after successful deletion?
= It's redirect success_url, such as "success_url = reverse_lazy("product_list)

"""





"""
Create / Update / Delete একসাথে
এখন আমাদের Product management অনেক পরিষ্কার:

CREATE:
/products/create/
       ↓
CreateView
       ↓
INSERT


READ:
/products/
       ↓
ListView


READ ONE:
/products/1/
       ↓
DetailView


UPDATE:
/products/1/edit/
       ↓
UpdateView
       ↓
UPDATE


DELETE:
/products/1/delete/
       ↓
DeleteView
       ↓
Confirmation
       ↓
POST
       ↓
DELETE


⭐ CRUD Complete
আমাদের Product CRUD এখন সম্পূর্ণ:

              PRODUCT CRUD
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    CREATE        READ        UPDATE
       │           │           │
 CreateView    ListView    UpdateView
                  │
             DetailView
                   │
                   ↓
                DELETE
                   │
              DeleteView

              
"""