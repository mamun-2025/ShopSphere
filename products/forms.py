

from django import forms 
from .models import Product
from categories.models import Category
from django.db.models import Q 
from django.core.validators import FileExtensionValidator
from .validators import validate_file_size

class ProductForm(forms.ModelForm):

      image = forms.ImageField(
            required=False,
            validators=[
               FileExtensionValidator(
                  allowed_extensions=["jpg", "jpeg", "png", "webp"]
               ),
               validate_file_size,
            ],
            widget=forms.ClearableFileInput(
               attrs={
                  "class": "form-control",
                  "accept": "image/jpeg,image/png,image/webp",
               }
            ),
         )
   
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
                  "step": "0.01",
               }
            ),

            "stock": forms.NumberInput(
               attrs={
                  "class": "form-control",
                  "placeholder": "Enter prodcut stock",
                  "min": 0,
                  "step": "1",
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


      def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        active_categories = Category.objects.filter(
            is_active=True
        )

        if self.instance.pk and self.instance.category_id:

            active_categories = Category.objects.filter(
                Q(is_active=True)
                | Q(pk=self.instance.category_id)
            )

        self.fields["category"].queryset = active_categories


      def clean_sku(self):
         sku = self.cleaned_data["sku"]

         return sku.strip()

   


   