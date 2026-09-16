

from django import forms 
from .models import Category

class CategoryForm(forms.ModelForm):
   class Meta:
      model = Category

      fields = [
         "name",
         "description",
         "is_active",
      ]

      widgets = {
         "name": forms.TextInput(
            attrs={
               "class": "form-control",
               "placeholder": "Enter category name",
            }
         ),
         "description": forms.Textarea(
            attrs={
               "class": "form-control",
               "placeholder": "Enter category description",
            }
         ),
         "is_active": forms.CheckboxInput(
            attrs={
               "class": "form-check-input",
            }
         ),
      }