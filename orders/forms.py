

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


class OrderCancellationRequestForm(forms.Form):
   reason = forms.CharField(
      label="Cancellation reason",
      min_length=5,
      max_length=1000,
      widget=forms.Textarea(
         attrs={
            "rows": 4,
            "placeholder": "Why do you want to cancel this order?",
            "class": "form-control",
         }
      ),
   )


class AdminCancellationReviewForm(forms.Form):
   admin_note = forms.CharField(
      label="Admin note",
      required=False,
      max_length=1000,
      widget=forms.Textarea(
         attrs={
            "rows": 3,
            "placeholder": "Optional review note...",
            "class": "form-control",
         }
      ),
   )

class AdminDirectCancellationForm(forms.Form):
   reason = forms.CharField(
      label="Cancellation reason",
      min_length=5,
      max_length=1000,
      widget=forms.Textarea(
         attrs={
            "rows": 4,
            "placeholder": "Explain why this order is being cancelled...",
            "class": "form-control",
         }
      ),
   )

   admin_note = forms.CharField(
      label="Internal admin note",
      required=False,
      max_length=1000,
      widget=forms.Textarea(
         attrs={
            "rows": 3,
            "placeholder": "Optional internal note...",
            "class": "form-control",
         }
      ),
   )
