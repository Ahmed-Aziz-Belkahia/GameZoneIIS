from django.contrib import admin
from vendor.models import Vendor, OrderTracker, DeliveryCouriers, PayoutTracker, Notification, ChatMessage, Coupon
from import_export.admin import ImportExportModelAdmin


class VendorAdmin(ImportExportModelAdmin):
    list_display = ['user', 'shop_name', 'vendor_image', 'payout_method' ,'total_payout_tracker', 'currency', 'verified', "product_count"]
    list_per_page = 1000
    search_fields  = ['shop_name', 'shop_email', 'id']
    
class DeliveryCouriersAdmin(ImportExportModelAdmin):
    list_display = ['couriers_name' , 'couriers_tracking_website_address']
    
class PayoutTrackerAdmin(ImportExportModelAdmin):
    list_display = ['vendor' , 'amount', 'item' ,'currency', 'date']
    
        
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ['user', 'user', 'product', 'order', 'bid', 'offer' ,'amount', 'type', 'seen']

    
class ChatMessageAdmin(ImportExportModelAdmin):
    list_display = ['user', 'sender', 'reciever' ,'message','date', 'is_read']
    
class CouponAdmin(ImportExportModelAdmin):
    list_editable = ['valid_from', 'valid_to' ,'code', 'active', 'type']
    list_display = ['vendor' ,'code', 'discount', 'type', 'redemption', 'valid_from', 'valid_to' , 'active', 'date']
        

admin.site.register(Vendor, VendorAdmin)
admin.site.register(DeliveryCouriers, DeliveryCouriersAdmin)
admin.site.register(PayoutTracker, PayoutTrackerAdmin)
# admin.site.register(OrderTracker)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Coupon, CouponAdmin)
    