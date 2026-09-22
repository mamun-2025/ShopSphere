

from django import forms 
from .models import Product

class ProductForm(forms.ModelForm):
   
   class Meta:
      model = Product

      fields = [
         "name",
         "category",
         "brand",
         "description",
         "sku",
         "price",
         "stock",
         "image",
         "manual",
         "is_active",
      ]

      widgets ={
         "name":forms.TextInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter product name",
            }
         ),

         "category": forms.Select(
            attrs={
               "class": "form-select",
            }
         ),

         "description": forms.Textarea(
            attrs={
               "class": "form-control",
               "rows": 5,
               "placeholder": "Enter product description",
            }
         ),

         "sku": forms.TextInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter sku",
            }
         ),

         "brand": forms.TextInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter brand",
            }
         ),

         "price": forms.NumberInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter product price",
               "min": 0,
            }
         ),

         "stock": forms.NumberInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter prodcut stock",
               "min": 0,
            }
         ),
         
         "image": forms.ClearableFileInput(
            attrs={
               "class": "form-control",
            }
         ),

         "manual": forms.ClearableFileInput(
            attrs={
               "class": "form-control",
               "accept": "application/pdf",
            }
         ),

         "is_active": forms.CheckboxInput(
            attrs={
               "class": "form-check-input",
            }
         ),

         
      }