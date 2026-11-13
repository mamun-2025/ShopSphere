

from django import forms 

from .models import Order

class AdminOrderStatusUpdateForm(forms.Form):

   status = forms.ChoiceField(
      choices=Order.Status.choices,
      required=True,
      widget=forms.Select(
         attrs={
            "class": "form-select",
         }
      ),
      label="New Order Status",
   )

   