from django import forms
from userauths.models import User, Profile
from django.forms import ImageField, FileInput, DateInput
from vendor.models import Coupon, Vendor, DeliveryCouriers
from store.models import Product, Brand, Gallery, CartOrder, CartOrderItem
from crispy_forms.helper import FormHelper
from django.forms import formset_factory, modelformset_factory, inlineformset_factory



class VendorForm(forms.ModelForm):
    shop_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Shop Name', 'class': 'form-control', 'id': ""}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Residential Address', 'class': 'form-control', 'id': ""}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control', 'id': ""}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State', 'class': 'form-control', 'id': ""}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'id': ""}))
    shop_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Shop Email Address', 'class': 'form-control', 'id': ""}))
    # shop_cover_image = ImageField(widget=FileInput)
    # shop_image = ImageField(widget=FileInput)
    # identity_image = ImageField(widget=FileInput)
    
    helper = FormHelper()
    
    class Meta:
        model = Vendor
        widgets = {
            'shop_cover_image': FileInput(attrs={'onchange': 'loadFile(event)'}),
            'shop_image': FileInput(attrs={'onchange': 'preview()'}),
            'identity_image': FileInput(attrs={'onchange': 'preview_id()'}),
        }
        fields = [
            'shop_name', 
            'shop_description' ,
            'gender',
            'identity_type',
            'identity_image', 
            'shop_image', 
            'show_email_address_in_store',
            'show_mobile_number_in_store',
            'shop_cover_image',
            'address', 
            'city' , 
            'mobile' , 
            'shop_email' ,
            'state', 
            'country' , 
            # 'currency',
            # 'payout_method',
            # 'paypal_email_address',
            'keywords',
            ]

class PayoutForm(forms.ModelForm):
    helper = FormHelper()
    
    class Meta:
        model = Vendor
        fields = [
            'currency',
            'payout_method',
            'paypal_email_address',
            ]

class DateInput(forms.DateInput):
    input_type = "date"

class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Product Title', 'class': 'form-control', 'id': ""}))
    product_condition_description = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Product Condition Description', 'class': 'form-control', 'id': ""}), required=False)
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Price', 'class': 'form-control', 'id': ""}), required=False)
    old_price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Old Price', 'class': 'form-control', 'id': ""}), required=False)
    shipping_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Shipping Amount Price', 'class': 'form-control', 'id': ""}), required=False)
    stock_qty = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Stock Amount', 'class': 'form-control', 'id': ""}), required=False)
    image = ImageField(widget=FileInput)
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price' ,'old_price','shipping_amount','category','brand', 'product_condition', 'product_condition_rating' ,'product_condition_description' ,'show_old_price' , 'tags' , 'stock_qty' , 'in_stock', 'type', 'ending_date']
        widgets = {
            'ending_date': DateInput(attrs={'class': 'd-nonfe'}),
        }

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image',]
        
    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'data-img-class'

GalleryDataFormSet = inlineformset_factory(
    Product, Gallery, form=GalleryForm,
    extra=2, can_delete=True, max_num=5,
    can_delete_extra=True
)

class DeliveryCouriersForm(forms.ModelForm):
    couriers_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Courier Name', 'class': 'form-control', 'id': ""}))
    couriers_tracking_website_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Courier Tracking Website Address', 'class': 'form-control', 'id': ""}))
    
    class Meta:
        model = DeliveryCouriers
        fields = ['couriers_name','couriers_tracking_website_address']
        
class CartOrderInvoiceForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Full Name', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Residential Address', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    town_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Country', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Country', 'class': 'form-control', 'id': ""}), max_length=1000, required=True)
    
    class Meta:
        model = CartOrder
        fields = ['full_name','email','mobile','address','town_city','state','country','postal_code',]
        
class CartOrderItemsInvoiceForm(forms.ModelForm):
    class Meta:
        model = CartOrderItem
        fields = ['qty','price','shipping','product_obj',]
        
    def __init__(self, *args, **kwargs):
        super(CartOrderItemsInvoiceForm, self).__init__(*args, **kwargs)
        # self.request = kwargs.pop("request")
        # self.fields['product_obj'].queryset = Product.objects.filter(user=user)
        
CartOrderItemDataFormSet = inlineformset_factory(
    CartOrder, CartOrderItem, form=CartOrderItemsInvoiceForm,
    extra=2, can_delete=True,
    can_delete_extra=True
)

class CartOrderForm(forms.ModelForm):

    class Meta:
        model = CartOrder
        fields = ['full_name','email','mobile','address','town_city','state','country','postal_code',]
       
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Buyer Full Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Mobile Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Home/Street Address'}),
            'town_city': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Town or City'}),
            'state': forms.TextInput(attrs={'class': 'form-control','placeholder': 'State'}),
            # 'country': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Postal Code'}),
        }
        
class CartOrderItemForm(forms.ModelForm):
    class Meta:
        model = CartOrderItem
        fields = ['qty','price','shipping','product_obj']

        widgets = {
            'qty': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Price'}),
            'shipping': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Shipping Price'}),
        }

CartOrderItemFormset = modelformset_factory(
    CartOrderItem,
        fields = ['qty','price','shipping','product_obj'],
        extra=1,
        widgets = {
            'qty': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Price'}),
            'shipping': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Shipping Price'}),
        }
)

class FilteredCartOrderItemFormset(CartOrderItemFormset):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Product.objects.filter(user=user)
        self.form.base_fields['product_obj'].queryset = queryset

class CouponApplyForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a coupon code', 'class': 'form-control', 'id': ""}))
    discount = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Enter discount amount', 'class': 'form-control', 'id': ""}))
    
    class Meta:
        model = Coupon
        fields = ['code', 'valid_from', 'discount' ,'valid_to', 'make_public']
        widgets = {
            'valid_from': DateInput(attrs={'class': ''}),
            'valid_to': DateInput(attrs={'class': ''}),
        }