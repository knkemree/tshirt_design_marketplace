from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    end_product_img = forms.CharField(required=False, widget=forms.HiddenInput)
    mockup = forms.CharField(required=False, widget=forms.HiddenInput)
    design = forms.CharField(required=False, widget=forms.HiddenInput)