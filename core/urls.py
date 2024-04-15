from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    #path("my-dashboard/", views.buyer_account, name="buyer-dashboard"),
    path("profile/", views.buyer_profile, name="profile"),
    path("settings/", views.buyer_profile_settings, name="settings"),
    path("my-orders/", views.buyer_orders, name="buyer-orders"),
    path("my-orders/<oid>/", views.buyer_order_detail, name="buyer-order-detail"),

    # Shipping Address
    path("my-address/", views.buyer_address, name="buyer-address"),
    path("my-address/edit/<id>/", views.buyer_edit_address, name="buyer-edit-address"),
    path("my-address/delete/<id>/", views.buyer_delete_address, name="buyer-delete-address"),

    # Billing Address
    path("my-billing-address/", views.buyer_billing_address, name="buyer-billing-address"),
    path("my-billing-address/edit/<id>/", views.buyer_edit_billing_address, name="buyer-edit-billing-address"),
    path("add_billing_address", views.add_billing_address, name="add_billing_address"),
    path("my-billing-address/delete/<id>/", views.buyer_delete_billing_address, name="buyer_delete_billing_address"),

    path("my-wishlist/", views.buyer_wishlist, name="buyer-wishlist"),
    path("my-invoices/", views.buyer_invoices, name="buyer-invoices"),
    path("my-invoice/<oid>/", views.buyer_invoice_detail, name="buyer-invoice-detail"),
    path("my-bids/", views.buyer_bids, name="buyer_bids"),
    path("my-bids-detail/<pid>/<bid>", views.buyer_bids_detail, name="buyer_bids_detail"),
    path("order-tracker/", views.buyer_track_order, name="order-tracker"),
    path("tracked-order/<oid>/", views.tracked_order, name="tracked-order"),
    path("buyer_offer", views.buyer_offer, name="buyer_offer"),
    path("buyer_offer_detail/<pid>/<oid>/", views.buyer_offer_detail, name="buyer_offer_detail"),
    path("cancel_order/<oid>/", views.cancel_order, name="cancel_order"),
    path("cancel_orderitem/", views.cancel_orderitem, name="cancel_orderitem"),

    # Messaging
    path('inbox/', views.inbox, name="buyer_message"),
    path('inbox/<username>/', views.get_inbox, name="inbox-detail"),
    path('send_message_ajax/<username>/', views.send_message_ajax, name="send_message_ajax"),
    path('search_user/', views.search_users, name="search_users"),

    # Ajax
    path("delete-wishlist/<id>/", views.delete_from_wishlist, name="delete-wishlist"),
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),
    path("make-default-address/", views.make_address_default, name="make-default-address"),
    path("make-billing-default-address/", views.make_billing_address_default, name="make-default-billing-address"),

]
