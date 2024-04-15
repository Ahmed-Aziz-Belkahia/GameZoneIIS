from django.urls import path
from userauths import views
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500


app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.Register, name="sign-up"),
    path("sign-in/", views.loginViewTemp, name="sign-in"),
    path("sign-in-2/", views.loginView, name="sign-in-2"),
    path("sign-out/", views.logoutView, name="sign-out"),
    path("vendor_sign_in/", views.loginAsVendor, name="vendor_sign_in"),
    path("check_email/", views.check_email, name="check_email"),
    
    
]
