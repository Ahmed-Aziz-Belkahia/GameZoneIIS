from django.urls import path
from addons import views

app_name = "addons"

urlpatterns = [
    path("contact_us/", views.contact_us, name="contact_us"),
    path("about_us/", views.about_us, name="about_us"),
    path("send_faq_qs/", views.send_faq_qs, name="send_faq_qs"),
    path("subscribe_to_newsletter/", views.subscribe_to_newsletter, name="subscribe_to_newsletter"),

    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_and_conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("return_policy/", views.return_policy, name="return_policy"),
    path("secure_purchases/", views.secure_purchases, name="secure_purchases"),
    
    #path("terms_of_sales/", views.terms_of_sales, name="terms_of_sales"),

    #path("ConditionsGeneralesvente/", views.ConditionsGeneralesvente, name="ConditionsGeneralesvente"),
    #path("Politiqueconfidentialite/", views.Politiqueconfidentialite, name="Politiqueconfidentialite"),
]
