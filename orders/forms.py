from django import forms
from .models import Order
class OrderCreateForm(forms.ModelForm):
    recipient = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = ['recipient','shipping_label']
