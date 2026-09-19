

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
         "is_active",
      ]
      widgets ={
         "name":forms.TelInput(
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
         "sku": forms.TelInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter sku"
            }
         ),
         "price": forms.NumberInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter product price",
            }
         ),
         "stock": forms.NumberInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter prodcut stock",
            }
         ),
         "is_active": forms.CheckboxInput(
            attrs={
               "class": "form-check-input",
            }
         ),
         
      }