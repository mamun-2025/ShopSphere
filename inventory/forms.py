
from django import forms


class StockAdjusmentForm(forms.Form):
   quantity = forms.IntegerField(
      min_value=1,
      label="Quantity",

      widget=forms.NumberInput(
         attrs={
            "class": "form-control",
            "placeholder": "Enter quantity",
            "min": 1,
         }
      ),
      
   )

