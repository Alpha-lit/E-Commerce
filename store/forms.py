from django import forms
from .models import *

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Customer
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'shipping_address_1',
            'shipping_address_2',
            'shipping_city',
            'shipping_state',
            'shipping_zip_code',
            'shipping_country'
        ]
        
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            return username
        raise forms.ValidationError("Username is already taken")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'order_total', 'payment_method', 'payment_data']
        widgets = {
            'payment_data': forms.Textarea(attrs={'rows': 4}),
        }

class AddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        min_value=0,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'})
    )
    update = forms.BooleanField(
        label='Update',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Card Number'}))
    shipping_address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Shipping Address'}))
    PAYMENT_METHOD_CHOICES = (
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('paypal', 'PayPal'),
)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))