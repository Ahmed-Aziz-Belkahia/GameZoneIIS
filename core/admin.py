from django.contrib import admin
from core.models import Address, Wishlist, CancelledOrder, BillingAddress

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['user', 'address', 'status', 'same_as_billing_address']

class BillingAddressAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['user', 'address', 'status']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']
    
class CancelledOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'orderitem', 'refunded']
    
    
admin.site.register(Address, AddressAdmin)
admin.site.register(CancelledOrder, CancelledOrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(BillingAddress, BillingAddressAdmin)
