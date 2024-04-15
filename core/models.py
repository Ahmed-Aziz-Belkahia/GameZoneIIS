
from django.db import models
from userauths.models import User
# from store.models import Product



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        if self.product.title:
            return self.product.title
        else:
            return "Wishlist"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    country = models.ForeignKey("addons.TaxRate", on_delete=models.SET_NULL, null=True, related_name="address_country", blank=True)

    state = models.CharField(max_length=100)
    town_city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    same_as_billing_address = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "Address"
        
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    # country = models.CharField(max_length=100)
    country = models.ForeignKey("addons.TaxRate", on_delete=models.SET_NULL, null=True, related_name="billing_country", blank=True)

    state = models.CharField(max_length=100)
    town_city = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Billing Address"

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "Billing Address"
        
class CancelledOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    orderitem = models.ForeignKey("store.CartOrderItem", on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=100)
    refunded = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Cancelled Order"

    def __str__(self):
        if self.user:
            return str(self.user.username)
        else:
            return "Cancelled Order"