from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 201)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int,
                                #widget=forms.Select(attrs={'onchange':'this.form.submit();'})
                                widget=forms.Select(attrs={'class':'form-control'})
                                )
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
    placement = forms.CharField(required=False, widget=forms.HiddenInput)
    technique = forms.CharField(required=False, widget=forms.HiddenInput)
    end_product_img = forms.CharField(required=False, widget=forms.HiddenInput)
    mockup = forms.CharField(required=False, widget=forms.HiddenInput)
    design = forms.CharField(required=False, widget=forms.HiddenInput)
    json_data = forms.JSONField(required=False, widget=forms.HiddenInput)
    