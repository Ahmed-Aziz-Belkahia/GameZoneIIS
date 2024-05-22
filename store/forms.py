from store.models import Review, CartOrderItem, CartOrder
from core.models import Address, BillingAddress
from django import forms

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = Review
        fields = ['review', 'rating']


class AddressForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)

    class Meta:
        model = Address
        fields = ['full_name','mobile','email','country' ,'state','town_city','zip','address', 'same_as_billing_address']


class BillingAddressForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':''}), required=True)

    class Meta:
        model = BillingAddress
        fields = ['full_name','mobile','email','country','state','town_city','zip','address']


class CartOrderItemForm(forms.ModelForm):
    tracking_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Tracking ID'}))

    class Meta:
        model = CartOrderItem
        fields = ['delivery_couriers', 'tracking_id']


class CheckoutForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Active Mobile Number'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valid Email Address'}), required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Town or City'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street and Home Address'}), required=True)

    billing_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required=False)
    billing_town_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Town or City'}), required=False)
    billing_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing Street and Home Address'}), required=False)

    shipping_method = forms.ChoiceField(choices=CartOrder.SHIPPING_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Shipping Method'}), required=True)
    payment_method = forms.ChoiceField(choices=CartOrder.PAYMENT_METHOD_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Payment Method'}), required=True)

    class Meta:
        model = CartOrder
        fields = ['full_name', 'mobile', 'email', 'country', 'state', 'town_city', 'address', 'postal_code', 
                  'billing_state', 'billing_town_city', 'billing_address', 'billing_postal_code', 'billing_country']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)

        # Set default country to the first one in the list
        default_country = self.fields['country'].queryset.first()
        self.fields['country'].initial = default_country

        if user:
            self.fields['full_name'].initial = user.profile.full_name
            self.fields['email'].initial = user.email
            self.fields['mobile'].initial = user.profile.phone
            self.fields['country'].initial = default_country
            self.fields['state'].initial = user.profile.state
            self.fields['town_city'].initial = user.profile.city
            self.fields['address'].initial = user.profile.address
            
            # Prefill billing address fields
            self.fields['billing_state'].initial = user.billing_state
            self.fields['billing_town_city'].initial = user.profile.city
            self.fields['billing_address'].initial = user.billing_address
            self.fields['billing_postal_code'].initial = user.profile.postal_code
            self.fields['billing_country'].initial = user.billing_country