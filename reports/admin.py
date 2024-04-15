from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from reports.models import GeneralIssue, OfferUserReport, ProductReport, BiddingUserReport, OrderItemReport, VendoReport


class VendorAdmin(ImportExportModelAdmin):
    list_editable = [ 'block_vendor', 'resolved']
    list_display = ['vendor', 'user', 'block_vendor', 'resolved', 'date']

class ProductReportAdmin(ImportExportModelAdmin):
    list_editable = [ 'disable_product', 'resolved']
    list_display = ['product', 'user', 'disable_product', 'resolved', 'date']
    
    
class BiddingUserReportAdmin(ImportExportModelAdmin):
    list_editable = [ 'block_user', 'resolved']
    list_display = ['product_bidding', 'vendor', 'block_user', 'resolved', 'date']
    
    
class OfferUserReportAdmin(ImportExportModelAdmin):
    list_editable = [ 'block_user', 'resolved']
    list_display = ['product_offer', 'vendor', 'block_user', 'resolved', 'date']
    

class OrderItemReportAdmin(ImportExportModelAdmin):
    list_editable = [ 'disable_product', 'block_vendor', 'resolved']
    list_display = ['order_item', 'user', 'disable_product', 'block_vendor', 'resolved', 'date']
    
    


admin.site.register(VendoReport, VendorAdmin)
admin.site.register(ProductReport, ProductReportAdmin)
admin.site.register(BiddingUserReport, BiddingUserReportAdmin)
admin.site.register(OfferUserReport, OfferUserReportAdmin)
admin.site.register(OrderItemReport, OrderItemReportAdmin)
admin.site.register(GeneralIssue)