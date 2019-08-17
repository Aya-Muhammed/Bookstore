from django import forms
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('CARD', 'Credit or debit card'),
    ('CASH', 'Cash on delivery'),
)


class UsernameUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']


class EmailUpdateForm(forms.ModelForm):
    email = forms.EmailField()


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'name',
        'placeholder': 'Your name',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'placeholder': 'Your email',
        'class': 'form-control'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'phone',
        'placeholder': 'Your phone number',
        'class': 'form-control'
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'subject',
        'placeholder': 'message subject',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'subject',
        'placeholder': 'message subject',
        'class': 'form-control md-textarea',
        'rows': 2
    }))


class CheckoutForm(forms.Form):
    city = forms.CharField(required=False)
    area = forms.CharField(required=False)
    street_name = forms.CharField(required=False)
    mobile = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
    phone = forms.CharField()
