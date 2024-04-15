from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from userauths.models import User, user_directory_path, Profile
from store import models as store_model
from django.db.models import Max
from django.core.validators import MinValueValidator, MaxValueValidator

IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
)

CURRENCY = (
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("GBP", "GBP"),
)

NOTIFICATION_TYPE = (
    ("new_order", "New Order"),
    ("new_offer", "New Offer"),
    ("new_bidding", "New Bidding"),
    
    ("item_arrived", "Item Arrived"),
    ("item_shipped", "Item Shipped"),
    ("item_delivered", "Item Delivered"),
    
    ("tracking_id_added", "Tracking ID Added"),
    ("tracking_id_changed", "Tracking ID Changed"),
    
    ("offer_rejected", "Offer Rejected"),
    ("offer_accepted", "Offer Accepted"),
    
    ("product_published", "Product Published"),
    ("product_rejected", "Product Rejected"),
    ("product_disabled", "Product Disabled"),
)

PAYOUT_METHOD = (
    ("payout_to_paypal", "Payout to Paypal"),
    ("payout_to_stripe", "Payout to Stripe"),
    ("payout_to_wallet", "Payout to Wallet"),
)

DISCOUNT_TYPE = (
    ("Percentage", "Percentage"),
    ("Flat Rate", "Flat Rate"),
)

# Create your models here.
class Vendor(models.Model):
    shop_cover_image = models.ImageField(upload_to=user_directory_path, default="shop-cover-image.jpg", blank=True, null=True)
    shop_image = models.ImageField(upload_to=user_directory_path, default="shop-image.jpg", blank=True, null=True)
    shop_name = models.CharField(max_length=100, help_text="Shop Name", blank=True, null=True)
    shop_description = CKEditor5Field(config_name='extends', default="", blank=True, null=True)
    shop_policy = CKEditor5Field(config_name='extends', default="", blank=True, null=True)
    shop_email = models.CharField(max_length = 150, default="")
    show_email_address_in_store = models.BooleanField(default=True, null=True)
    show_mobile_number_in_store = models.BooleanField(default=True, null=True)
    
    identity_image = models.ImageField(upload_to=user_directory_path, default="id.jpg", blank=True, null=True)
    identity_type = models.CharField(choices=IDENTITY_TYPE, default="national_id_card", max_length=100, blank=True, null=True)
    
    mobile = models.CharField(max_length = 150, default="", blank=True, null=True)
    gender = models.CharField(max_length =10, choices=GENDER, default="male", blank=True, null=True)
    # country = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey("addons.TaxRate", on_delete=models.SET_NULL, null=True, related_name="vendor_country", blank=True)
    city = models.CharField(max_length=100, default="", blank=True, null=True)
    state = models.CharField(max_length=100, default="", blank=True, null=True)
    address = models.CharField(max_length=1000, default="", blank=True, null=True)
    
    currency = models.CharField(max_length=40, default="USD", choices=CURRENCY)
    payout_method = models.CharField(max_length=200, default="payout_to_wallet", choices=PAYOUT_METHOD)
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="vendor")
    profile = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, related_name="vendor_profile")
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    # personaldestiny@gmail.com
    paypal_email_address = models.CharField(max_length=1000, null=True, blank=True)
    
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_payout_tracker = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    stripe_access_token = models.CharField(max_length=10000, null=True, blank=True)
    stripe_user_id = models.CharField(max_length=10000, null=True, blank=True)
    stripe_refresh_token = models.CharField(max_length=10000, null=True, blank=True)

    followers = models.ManyToManyField(User,blank=True, related_name="vendor_followers")
    keywords = models.CharField(max_length = 1000, help_text="Add keywords related to your shop, this would help buyers locate your shop", blank=True, null=True)
    password = models.CharField(max_length=10000, null=True, blank=True)
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('  <img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.shop_image.url))

    def vendor_wallet(self):
        return self.profile.wallet
    
    def __str__(self):
        if self.shop_name:
            return self.shop_name
        else:
            return "User"
        
    def rating_count(self):
        rating_count = store_model.Review.objects.filter(product__vendor=self, active=True).count()
        return rating_count
    
    def product_count(self):
        product_count = store_model.Product.objects.filter(vendor=self, status="published").count()
        return product_count
        
        
class OrderTracker(models.Model):
    order_item = models.ForeignKey('store.CartOrderItem', on_delete=models.CASCADE, blank=True, null=True, related_name="cartorderitem_tracker")
    status = models.CharField(max_length=5000, null=True, blank=True)
    location = models.CharField(max_length=5000, null=True, blank=True)
    activity = models.CharField(max_length=5000, null=True, blank=True)
    date= models.DateField(auto_now_add=True)

def __str__(self):
    return self.order_item


class DeliveryCouriers(models.Model):
    couriers_name = models.CharField(max_length=1000)
    couriers_tracking_website_address = models.URLField(null=True, blank=True)

    did = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Delivery Couriers"

    def __str__(self):
        return self.couriers_name
    

# Create your models here.
class PayoutTracker(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=40, default="USD", null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    item = models.ForeignKey('store.CartOrder', on_delete=models.SET_NULL, null=True, blank=True)
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.vendor)
    
    class Meta:
        ordering = ['-date']
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="notification_user")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True, related_name="notification_user")
    order = models.ForeignKey('store.CartOrder', on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey('store.ProductOffers', on_delete=models.CASCADE, null=True, blank=True)
    bid = models.ForeignKey('store.ProductBidders', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    type = models.CharField(max_length=100, default="new_order", choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    nid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.vendor)
    
    class Meta:
        ordering = ['-date']
    

    
    

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    message = models.CharField(max_length=10000000000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    mid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    
    
    
class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="coupon_vendor")
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    type = models.CharField(max_length=100, choices=DISCOUNT_TYPE, default="Percentage")
    discount = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    redemption = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    make_public = models.BooleanField(default=False)
    valid_from = models.DateField()
    valid_to = models.DateField()
    cid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")

    def save(self, *args, **kwargs):
        new_discount = self.discount / 100
        self.get_percent = new_discount
        
        super(Coupon, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.code
    
    class Meta:
        ordering =['-id']