
from django import forms 

class CartQuantityForm(forms.Form):

   quantity = forms.IntegerField(
      min_value=1,
      label="quantity",
      widget=forms.NumberInput(
         attrs={
            "class":"form-control",
            "min":1,
         }
      ),

   )