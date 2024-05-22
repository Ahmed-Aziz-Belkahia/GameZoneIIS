from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
import logging


from PIL import Image
from shortuuid.django_fields import ShortUUIDField

IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

GENDER = (
    ("F", "Female"),
    ("M", "Male"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gz_coins = models.IntegerField(default=0, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    roles = models.CharField(max_length=100, null=True, blank=True)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    billing_first_name = models.CharField(max_length=500, null=True, blank=True)
    billing_last_name = models.CharField(max_length=500, null=True, blank=True)
    billing_email = models.CharField(max_length=500, null=True, blank=True)
    billing_phone = models.CharField(max_length=500, null=True, blank=True)
    billing_address = models.CharField(max_length=500, null=True, blank=True)
    billing_state = models.CharField(max_length=500, null=True, blank=True)
    billing_country = models.CharField(max_length=500, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the object is already in the database (updating)
            original = User.objects.get(pk=self.pk)
            if self.gz_coins != original.gz_coins:
                print(f"gz_coins changed from {original.gz_coins} to {self.gz_coins} for user {self.username}")
        
        super(User, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if self.roles == "wcfm_vendor":
    #         "vendor.Vendor".objects.create(user=self, profile=None)
    #     else:
    #         self.product.status = "published"
    #         self.product.save()
            
    #     super(User, self).save(*args, **kwargs) 



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover.jpg", blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)


    country = models.ForeignKey("addons.TaxRate", on_delete=models.SET_NULL, null=True, related_name="user_country_tax", blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    postal_code = models.CharField(max_length=1000, null=True, blank=True)
    
    identity_type = models.CharField(choices=IDENTITY_TYPE, default="national_id_card", max_length=100, null=True, blank=True)
    identity_image = models.ImageField(upload_to=user_directory_path, default="id.jpg", null=True, blank=True)

    facebook = models.URLField(default="https://facebook.com/", null=True, blank=True)
    instagram = models.URLField(default="https://instagram.com/", null=True, blank=True)
    twitter = models.URLField(default="https://twitter.com/", null=True, blank=True)
    whatsApp = models.CharField(default="+123 (456) 789", max_length=100, blank=True, null=True)

    verified = models.BooleanField(default=False)
    seller = models.BooleanField(default=False)
    subscribed_newsletter = models.BooleanField(default=False)

    referral_earning = models.DecimalField(default=0.00, decimal_places=2, max_digits=12)
    wallet = models.DecimalField(default=0.00, decimal_places=2, max_digits=12)

    account_number = ShortUUIDField(length=10, max_length=25, alphabet="1234567890")
    pin = ShortUUIDField(length=4, max_length=6, alphabet="1234567890")
    code = models.CharField(max_length=12, blank=True, null=True)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='ref_by')
    
    saved_product = models.ManyToManyField("store.Product",blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"


    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image.path)
    #     if img.height > 700 or img.width > 700:
    #         output_size = (700, 700)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    #     super().save(*args, **kwargs)

    
    def profile_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" />' % (self.image))

    
    
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)






# class User(AbstractUser):
#     email = models.EmailField(null=True, blank=True)
#     username = models.CharField(max_length=100, null=True, blank=True)
#     full_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
#     bio = models.CharField(max_length=100, null=True, blank=True)
#     roles = models.CharField(max_length=100, null=True, blank=True)
#     total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#     billing_first_name = models.CharField(max_length=500, null=True, blank=True)
#     billing_last_name = models.CharField(max_length=500, null=True, blank=True)
#     billing_email = models.CharField(max_length=500, null=True, blank=True)
#     billing_phone = models.CharField(max_length=500, null=True, blank=True)
#     billing_address = models.CharField(max_length=500, null=True, blank=True)
#     billing_state = models.CharField(max_length=500, null=True, blank=True)
#     billing_country = models.CharField(max_length=500, null=True, blank=True)

#     USERNAME_FIELD = "full_name"
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username