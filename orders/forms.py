from django import forms
from .models import Order
from django.forms.widgets import Textarea
class OrderCreateForm(forms.ModelForm):
    recipient = forms.CharField(required=False)

    class Meta:
        model = Order
        
        fields = ['recipient','shipping_label','note']
        widgets = {
            'note': Textarea(attrs={'cols': 30, 'rows': 6}),
        }
