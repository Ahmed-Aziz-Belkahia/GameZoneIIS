from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe


STATUS = (
    ("live", "Live"),
    ("maintainance", "Maintainance"),
    ("error", "Error"),
)

REG_FORM = (
    ("classic", "Classic"),
    ("dynamic", "Dynamic"),
)

SERVICE_FEE_CHARGE_TYPE = (
    ("percentage", "Percentage"),
    ("flat_rate", "Flat Rate"),
)


CONTACT_REASON = (
    ("talk_to_an_agent ", "Talk To An Agent "),
    ("complaint", "Complaint"),
    ("report_product", "Report Product"),
    ("report_vendor", "Report Vendor"),
    ("new_feature_idea", "New Feature Idea"),
)



HOMEPAGE_STYLE_2 = (
    ("1", "Homepage 1"),
    ("2", "Homepage 2"),
    ("3", "Homepage 3"),
    ("4", "Homepage 4"),
    
)

LOGO_TYPE = (
    ("use_image ", "Use Company Image"),
    ("use_name ", "Use Company Name"),
    ("use_landscape ", "Use Landscape Image"),
    
)

REVIEW_TYPE = (
    ("any_authenticated_user ", "Allow any user that is logged in to review a product"),
    ("only_purchased_user ", "Allow only users who have purchased a product to review the product"),
)

NAVIGATION_BAR_STYLE = (
    ('1', "Header 1"),
    ('2', "Header 2"),
)


PRODUCT_PAYMENT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),
    ("Cash On Delivery", "Cash On Delivery"),
    
)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = ("Payment Method")
        verbose_name_plural = ("Payment Method")
        ordering = ['-date']

    def __str__(self):
        return self.name

class BasicAddon(models.Model):
    view_more = models.CharField(default="View All", max_length=10)
    service_fee_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)ve.g 4%")
    service_fee_flat_rate = models.DecimalField(default=0.7, max_digits=12, decimal_places=2 ,help_text="NOTE: Add the amount you want to charge as service fee e.g $2.30")
    service_fee_charge_type = models.CharField(default="percentage", max_length=30, choices=SERVICE_FEE_CHARGE_TYPE)
    
    affiliate_commission_percentage = models.IntegerField(default=50, help_text="NOTE: Numbers added here are in percentage (%)")
    general_tax_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)")
    vendor_fee_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)")
    currency_sign = models.CharField(default="$", max_length=10)
    currency_abbreviation = models.CharField(default="USD", max_length=10)
    registration_form_type = models.CharField(max_length=50, choices=REG_FORM, default="classic")
    send_email_notifications = models.BooleanField(default=False)
    payout_vendor_fee_immediately = models.BooleanField(default=True)
    payment_method = models.ManyToManyField(PaymentMethod, blank=True)
    review_type = models.CharField(default="any_authenticated_user", max_length=130, choices=REVIEW_TYPE)
    header_type = models.CharField(default='1', max_length=130, choices=NAVIGATION_BAR_STYLE)
    image_upload_limit = models.IntegerField(default=10)
    
    class Meta:
        verbose_name = ("Basic Addons")
        verbose_name_plural = ("Basic Addons")


        

class Policy(models.Model):
    #Politique de Confidentialite
    privacy_policy = CKEditor5Field(null=True, blank=True, config_name='extends')

    #Conditions Generales de vente
    terms_and_conditions = CKEditor5Field(null=True, blank=True, config_name='extends')

    #Expedition & retour
    return_policy = CKEditor5Field(null=True, blank=True, config_name='extends')

    #Achats securises
    secure_purchases = CKEditor5Field(null=True, blank=True, config_name='extends')

    
    class Meta:
        verbose_name = ("Policy")
        verbose_name_plural = ("Policy")

    def __str__(self):
        return "Policy"
    

class AboutUS(models.Model):
    about_us = CKEditor5Field(null=True, blank=True, config_name='extends')
    
    class Meta:
        verbose_name = ("About Us")
        verbose_name_plural = ("About Us")

    def __str__(self):
        return "About Us"
    


class EarningPoints(models.Model):
    signup_point = models.IntegerField(default=10)
    enable_signup_point = models.BooleanField(default=True)
    text = models.CharField(default="Point", max_length=10 )
    referral_point = models.PositiveIntegerField(default=500, help_text="Enter an amount that user will get when they refer thier friend")

    
    class Meta:
        verbose_name_plural = ("Earning Points")
        
    def __str__(self):
        return "Earning Points"

class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Company(models.Model):
    logo = models.ImageField(default="logo.jpg")
    logo_type = models.CharField(default="use_image", max_length=30, choices=LOGO_TYPE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    website_address = models.CharField(max_length=500, help_text="Add the website address without the slash /")
    admin_website_address = models.CharField(max_length=500, help_text="Add the admin address without the slash /")
    footer = models.CharField(max_length=1000)
    facebook = models.CharField(default="https://facebook.com/", max_length=1000)
    instagram = models.CharField(default="https://instagram.com/", max_length=1000)
    twitter = models.CharField(default="https://twitter.com/", max_length=1000)
    linkedin = models.CharField(default="https://linkedin.com/", max_length=1000)
    youtube = models.CharField(default="https://youtube.com/", max_length=1000)
    telegram = models.CharField(default="https://telegram.com/", max_length=1000)
    homepage = models.CharField(choices=STATUS, max_length=1000, default="live")
    secret_key = models.CharField(max_length=1000, null=True, blank=True)
    public_key = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return f"{self.name}"
    
    

class SupportContactInformation(models.Model):
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=1000, null=True, blank=True)
    working_days = models.CharField(max_length=1000, null=True, blank=True, default="Monday - Friday")
    open_time = models.CharField(max_length=100, null=True, blank=True, default="08 AM")
    closing_time = models.CharField(max_length=100, null=True, blank=True, default="05 PM")
    
    class Meta:
        verbose_name_plural = "Support Contact Information"

    def __str__(self):
        return f"Support Contact Information"
    
    
class TaxRate(models.Model):
    country = models.CharField(max_length=200)
    rate = models.IntegerField(default=5, help_text="Numbers added here are in percentage (5 = 5%)")
    active = models.BooleanField(default=True)
    custom_name = models.CharField(default="Tax", max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Tax Rates"

    def __str__(self):
        return f"{self.country}"
    
    
class SuperUserSignUpPin(models.Model):
    pin = models.CharField(default="17880984243324543", max_length=100)

    def __str__(self):
        return self.pin
    
    

class ContactUs(models.Model):
    cid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")
    product = models.ForeignKey("store.Product", on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=50, choices=CONTACT_REASON, default="talk_to_an_agent")
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Us "

    def __str__(self):
        return f"{self.full_name}"
    
    

class FAQs(models.Model):
    fid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True, blank=True)
    share = models.BooleanField(default=False)
    email = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = ("FAQs")
        verbose_name_plural = ("FAQs")

    def __str__(self):
        return self.question
    
    
class Announcements(models.Model):
    announcement_for_logged_in_users = CKEditor5Field(null=True, blank=True, config_name='extends')
    active_for_logged_in_user = models.BooleanField(default=False)
    
    announcement_for_not_logged_in_users = CKEditor5Field(null=True, blank=True, config_name='extends')
    active_for_not_logged_in_user = models.BooleanField(default=False)

    def __str__(self):
        return "Announcement"

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        


class PlatformNotifications(models.Model):
    image = models.ImageField(upload_to="notifications", null=True, blank=True)
    title = models.CharField(max_length=1000)
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")

    class Meta:
        verbose_name = ("Platform Update Notifications")
        verbose_name_plural = ("Platform Update Notifications")
        ordering = ['date']

class TutorialVideo(models.Model):
    title = models.CharField(default="Video Links", max_length=100)
    how_to_use_platform = models.URLField(default="https://youtube.com", null=True, blank=True)
    how_to_use_affiliate_system = models.URLField(default="https://youtube.com", null=True, blank=True)
    how_to_become_a_vendor = models.URLField(default="https://youtube.com", null=True, blank=True)
    
    class Meta:
        verbose_name = ("Tutorial Video")
        verbose_name_plural = ("Tutorial Video")



        
        
class HomePageSetup(models.Model):
    title = models.CharField(default="Home Page Setup", max_length=50)
    homepage_type = models.CharField(default="1", max_length=50, choices=HOMEPAGE_STYLE_2)
    
    class Meta:
        verbose_name_plural = ("Home Page Setup")
        


class Home_One(models.Model):
    homepage = models.ForeignKey(HomePageSetup, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="homepage", blank=True, null=True)
    small_title = models.CharField(default="Hey there, Welcome!", max_length=1010)
    main_title = models.CharField(default="Keep your new born baby engaged", max_length=1010)
    sub_title = models.CharField(default="Lorem Ipsum is the best way of writing destiny car type", max_length=1010)
    button_text = models.CharField(default="Shop Now", max_length=100)
    button_url = models.URLField(default="https://Desphixs.com/shop/", max_length=1000)
    first = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = ("Home One")
        
    def home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))


class Home_Two(models.Model):
    homepage = models.ForeignKey(HomePageSetup, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="homepage", blank=True, null=True)
    small_title = models.CharField(default="Hey there, Welcome!", max_length=1010)
    main_title = models.CharField(default="Keep your new born baby engaged", max_length=1010)
    sub_title = models.CharField(default="Lorem Ipsum is the best way of writing destiny car type", max_length=1010)
    button_text = models.CharField(default="Shop Now", max_length=100)
    button_url = models.URLField(default="https://Desphixs.com/shop/", max_length=1000)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = ("Home Two")
        
    def home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))
