from django.contrib import admin
from addons.models import AboutUS, BasicAddon, Company, PaymentMethod ,EarningPoints, NewsLetter, Policy, TaxRate, SuperUserSignUpPin, ContactUs, FAQs, Announcements, PlatformNotifications, TutorialVideo, SupportContactInformation, HomePageSetup, Home_One, Home_Two
from import_export.admin import ImportExportModelAdmin


class BasicAddonsAdmin(ImportExportModelAdmin):
    list_editable = ['service_fee_percentage', 'affiliate_commission_percentage', 'currency_abbreviation', 'vendor_fee_percentage', 'registration_form_type', 'header_type' ,'send_email_notifications', 'payout_vendor_fee_immediately']
    list_display = ['view_more', 'currency_sign', 'service_fee_percentage', 'affiliate_commission_percentage', 'currency_abbreviation', 'vendor_fee_percentage', 'registration_form_type', 'header_type' ,'send_email_notifications', 'payout_vendor_fee_immediately']



class EarningPointsAdmin(ImportExportModelAdmin):
    list_display = ['signup_point', "enable_signup_point"]

class HomeOne_Tab(admin.TabularInline):
    model = Home_One

class HomeTwo_Tab(admin.TabularInline):
    model = Home_Two

class HomePageSetupAdmin(ImportExportModelAdmin):
    inlines = [HomeOne_Tab, HomeTwo_Tab]
    list_editable = ['homepage_type']
    list_display = ['title', "homepage_type"]


class HomeOneAdmin(ImportExportModelAdmin):
    list_editable = ['small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active', 'first']
    list_display = ['homepage', "home_image", 'small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active', 'first']

class HomeTwoAdmin(ImportExportModelAdmin):
    list_editable = ['small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active']
    list_display = ['homepage', "home_image", 'small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active']


class NewsLetterAdmin(ImportExportModelAdmin):
    list_display = ['email']


class CompanyAdmin(ImportExportModelAdmin):
    list_editable = ['website_address', 'homepage', 'logo_type']
    list_display = ['name', 'website_address', 'homepage', 'logo_type']
    
class TaxRateAdmin(ImportExportModelAdmin):
    search_fields = ['country', 'custom_name']
    list_editable = ['rate', 'custom_name', 'active']
    list_display = ['country', 'rate', 'custom_name', 'active']
    
    
class ContactUsAdmin(ImportExportModelAdmin):
    list_editable = ['resolved']
    list_display = ['topic', 'full_name', 'email', 'subject', 'resolved', 'date']

class FAQsAdmin(ImportExportModelAdmin):
    list_editable = ['share']
    list_display = ['question', 'answer', 'email', 'share']


class PlatformNotificationsAdmin(ImportExportModelAdmin):
    list_display = ['title', 'active']

class TutorialVideoAdmin(ImportExportModelAdmin):
    list_editable = ['how_to_use_platform', 'how_to_use_affiliate_system', 'how_to_become_a_vendor']
    list_display = ['title', 'how_to_use_platform', 'how_to_use_affiliate_system', 'how_to_become_a_vendor']




admin.site.register(BasicAddon, BasicAddonsAdmin)
admin.site.register(Company, CompanyAdmin)
# admin.site.register(EarningPoints, EarningPointsAdmin)
admin.site.register(NewsLetter, NewsLetterAdmin)
admin.site.register(Policy)
admin.site.register(AboutUS)
# admin.site.register(SuperUserSignUpPin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQs, FAQsAdmin)
admin.site.register(Announcements)
admin.site.register(PlatformNotifications, PlatformNotificationsAdmin)
admin.site.register(SupportContactInformation)
admin.site.register(TaxRate, TaxRateAdmin)
admin.site.register(HomePageSetup, HomePageSetupAdmin)
admin.site.register(Home_One, HomeOneAdmin)
admin.site.register(Home_Two, HomeTwoAdmin)
admin.site.register(PaymentMethod)