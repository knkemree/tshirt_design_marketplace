from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField, UserCreationForm, UsernameField 
from django.db import transaction
from .models import Customer
from django.forms import CharField,  ModelForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    seller = forms.BooleanField(required = False)

    class Meta:
        model = Customer
        fields = ('first_name','last_name','email','password','password2','seller')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Customer.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # @transaction.atomic
    # def save(self, commit=True):
    #     user = super().save(commit=False)   
    #     user.buyer = True
    #     if commit:
    #         user.save()
    #     return user

class LoginForm(forms.Form): # Note: forms.Form NOT forms.ModelForm
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email','placeholder':'Email'}), 
        label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password','placeholder':'Password'}),
        label='Password')
    remember_me = forms.BooleanField( widget=forms.CheckboxInput())

    class Meta:
        fields = ['email', 'password','remember_me']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(),required=False)



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control','type':'text','name': 'email','id':'reg-email','required':'True'}), 
        label='Email')
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'name':'password1','required':'True', 'id':'reg-password'}), 
        )
    password2 = forms.CharField(
        label='Password confirmation', 
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'name':'password2','required':'True', 'id':'reg-password-confirm'}), 
        )

    seller = forms.BooleanField(
        label='Are you a seller?',
        widget=forms.CheckboxInput(),
        required=False
    )
    
    class Meta:
        model = Customer
        fields = ('email','password1','password2','seller',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #user.buyer = True
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = ('email', 'password', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UpdateCreditForm(forms.Form):
    amount = forms.DecimalField(max_digits=10,decimal_places=2, min_value=0.00)

