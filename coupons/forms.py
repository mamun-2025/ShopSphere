

from django import forms 

class CouponApplyForm(forms.Form):
   code = forms.CharField(
      max_length=50,
      required=True,
      strip=True,
      widget=forms.TextInput(
         attrs={
            "placeholder": "Enter your coupon code",
            "class": "form-control",
            "autocomplete": "off",
         }
      ),
      error_messages={
         "required": "Please enter a coupon code.",
         "max_length": "Coupon code is too long.",
      },
   )

   def clean_code(self):
      return self.cleaned_data["code"].upper()
   