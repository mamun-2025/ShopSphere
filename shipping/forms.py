

from django import forms
from .models import  ShippingAddress, ShippingMethod, ShippingZone


class ShippingAddressForm(forms.ModelForm):
   class Meta:
      model = ShippingAddress

      fields = [
         "full_name",
         "phone",
         "address_line",
         "zone",
         "area",
         "city_or_district",
         "postal_code",
         "delivery_instructions",
      ]

      widgets = {
         "full_name": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "phone": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "address_line": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "zone": forms.Select(
            attrs={
               "class": "form-select"
            }
         ),
         "area": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "city_or_district": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "postal_code": forms.TextInput(
            attrs={
               "class": "form-control"
            }
         ),
         "delivery_instructions": forms.Textarea(
            attrs={
               "class": "form-control",
               "rows": 2,
            }
         ),

      }

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      self.fields["zone"].queryset = ShippingZone.objects.filter(
         is_active=True
      )
      self.fields["zone"].empty_label = "Choose delivery zone"
      self.fields["zone"].required = True



class ShippingMethodForm(forms.Form):
   shipping_method = forms.ModelChoiceField(
      queryset=ShippingMethod.objects.none(),
      empty_label=None,
      widget=forms.RadioSelect,
      label="Choose a delivery method",
   )

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      self.fields["shipping_method"].queryset = (
         ShippingMethod.objects.filter(is_active=True)
         .select_related("zone")
      )







