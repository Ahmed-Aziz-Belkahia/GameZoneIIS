from django.contrib import admin
from userauths.models import User, Profile
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelChoiceField

class StaffUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class CustomUserAdmin(UserAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
            kwargs['form_class'] = StaffUserChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class UserAdmin(admin.ModelAdmin):
    search_fields  = ['username', 'email', 'id']
    list_filter = ['roles']
    list_display = ['username', 'email', 'roles', 'id', 'gz_coins']
    list_per_page = 500

class ProfileAdmin(admin.ModelAdmin):
    search_fields  = ['user', 'shop_name']
    list_display = ['user', 'full_name', 'profile_image', 'wallet']
    list_per_page = 1000

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)