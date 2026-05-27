from django import forms
from .models import Product, Buyer
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('buyer','Buyer'),('seller','Seller')])

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    quantity = forms.IntegerField()
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)

class BuyNowForm(forms.Form):
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    delivery_instructions = forms.CharField(widget=forms.Textarea, required=False)
 
