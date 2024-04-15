from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User




# Create your models here.
class VendoReport(models.Model):
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="vendor_report")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="vendor_reporting_user")
    
    message = models.TextField(null=True, blank=True)
    block_vendor = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Vendor Report"

    def __str__(self):
        return str(self.user)
       
        
        
class ProductReport(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.SET_NULL, null=True, related_name="product_report")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="product_reporting_user")
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="product_vendor_report")

    message = models.TextField(null=True, blank=True)
    disable_product = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Report"

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        if self.disable_product == True:
            self.product.status = "disabled"
            self.product.save()
        else:
            self.product.status = "published"
            self.product.save()
            
        super(ProductReport, self).save(*args, **kwargs) 
    
    
class BiddingUserReport(models.Model):
    product_bidding = models.ForeignKey("store.ProductBidders", on_delete=models.SET_NULL, null=True, related_name="bidding_report")
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="bidding_reporting_user")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bidding_reporting_user")
    message = models.TextField(null=True, blank=True)
    block_user = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Bidding User Report"

    def __str__(self):
        return str(self.vendor)
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        if self.block_user == True:
            self.product_bidding.user.is_active = False
            self.product_bidding.user.save()
        else:
            self.product_bidding.user.is_active = True
            self.product_bidding.user.save()
            
        super(BiddingUserReport, self).save(*args, **kwargs) 



class OfferUserReport(models.Model):
    product_offer = models.ForeignKey("store.ProductOffers", on_delete=models.SET_NULL, null=True, related_name="offer_report")
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="offer_reporting_user")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="offer_reporting_user")
    message = models.TextField(null=True, blank=True)
    block_user = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Offer User Report"

    def __str__(self):
        return str(self.vendor)
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        if self.block_user == True:
            self.product_offer.user.is_active = False
            self.product_offer.user.save()
        else:
            self.product_offer.user.is_active = True
            self.product_offer.user.save()
            
        super(BiddingUserReport, self).save(*args, **kwargs)
    

class OrderItemReport(models.Model):
    order_item = models.ForeignKey("store.CartOrderItem", on_delete=models.SET_NULL, null=True, related_name="order_item_report")
    user = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, related_name="order_item_reporting_user")
    
    message = models.TextField(null=True, blank=True)
    block_vendor = models.BooleanField(default=False)
    disable_product = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Order Item Report"

    def __str__(self):
        return str(self.user.username)
    

class GeneralIssue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="general_issueuser")
    message = models.TextField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "General Report"

    def __str__(self):
        return str(self.user.username)