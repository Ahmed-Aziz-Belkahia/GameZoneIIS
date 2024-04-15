from store.models import Review, CartOrderItem, CartOrder
from core.models import Address, BillingAddress
from django import forms

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = Review
        fields = ['review', 'rating']


class AddressForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)

    class Meta:
        model = Address
        fields = ['full_name','mobile','email','country' ,'state','town_city','zip','address', 'same_as_billing_address']


class BillingAddressForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':''}), required=True)

    class Meta:
        model = BillingAddress
        fields = ['full_name','mobile','email','country','state','town_city','zip','address']
        
        
        
class CartOrderItemForm(forms.ModelForm):
    tracking_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Enter Tracking ID'}))


    class Meta:
        model = CartOrderItem
        fields = ['delivery_couriers', 'tracking_id']


        
class CheckoutForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Full Name'}), required=False)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Active Mobile Number'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Valid Email Address'}), required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'State'}), required=False)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Town or City'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Street and Home Address'}), required=False)

    billing_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Billing State'}), required=False)
    billing_town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Billing Town or City'}), required=False)
    billing_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':' Billing Street and Home Address'}), required=False)

    shipping_method = forms.ChoiceField(choices=CartOrder.SHIPPING_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': "", 'placeholder':'Shipping Method'}), required=True)
    payment_method = forms.ChoiceField(choices=CartOrder.PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': "", 'placeholder':'Payment Method'}), required=True)

    class Meta:
        model = CartOrder
        fields = ['full_name','mobile','email','country','state','town_city','address', 'postal_code' ,'billing_state','billing_town_city','billing_address', 'billing_postal_code' ,'billing_country']
        