from django.urls import path
from vendor import views

app_name = "vendor"

urlpatterns = [
    path("become-a-vendor/", views.become_a_vendor, name="become-vendor"),
    path("registration/", views.VendorRegister, name="vendor-registration"),
    path("dashboard/", views.vendor_dashboard, name="dashboard"),
    path("revenue_summary/", views.revenue_summary, name="revenue_summary"),

    path('orders/', views.vendor_orders, name='orders'),
    path("order-detail/<oid>/", views.vendor_order_detail, name="order-detail"),
    path("order/status/<status>/", views.order_delivery_status, name="order-delivery-status"),
    
    path("earning/", views.vendor_earning, name="earning"),
    path("settings/", views.vendor_shop_creation, name="settings"),
    path("vendor_payout_update/", views.vendor_payout_update, name="vendor_payout_update"),
    
    path("products/", views.vendor_products, name="products"),
    path("products/category/<cid>/", views.vendor_product_category, name="product-category"),
    path("products/status/<status>/", views.vendor_product_status, name="product-status"),
    path("add-product/", views.vendor_add_product, name="add-product"),
    
    # Reviews
    path("reviews/", views.vendor_review, name="reviews"),
    path("send_reply/", views.send_reply, name="send_reply"),
    
    # PRoduct Faq
    path("faqs/", views.vendor_faq, name="vendor_faq"),
    path("send_answer/", views.send_answer, name="send_answer"),
    
    path("edit-product/<pid>/", views.vendor_edit_product, name="edit-product"),
    path('create-product/', views.ProductCreate.as_view(), name='create_product'),
    path('update-product/<int:pk>/', views.ProductUpdate.as_view(), name='update_product'),
    
    # Bidding
    path("product_bidding/", views.product_biddings, name="product_bidding"),
    path("product_bidding_detail/<pid>", views.product_bidding_detail, name="product_bidding_detail"),
    
     # Bidding
    path("product_offers/", views.product_offers, name="product_offers"),
    path("product_offer_detail/<pid>", views.product_offer_detail, name="product_offer_detail"),
    path("mark_as_accepted/", views.mark_as_accepted, name="mark_as_accepted"),
    path("mark_as_rejected/", views.mark_as_rejected, name="mark_as_rejected"),
    
    
    # Add Order Tracking ID
    path('add-trackingID/<coid>/<oid>/', views.add_tracking_id, name='add-trackingID'),
    
    # Custom ORder Invoice
    path('create-order-invoice/', views.CartOrderCreate.as_view(), name='create-order-invoice'),
    path('create-order-item-invoice/<oid>/', views.create_order_item_invoice, name='create-order-item-invoice'),
    path('create_custom_order_with_items/', views.create_custom_order_with_items, name='create_custom_order_with_items'),
    path('list_custom_order/', views.list_custom_order, name='list_custom_order'),
    path('invoice_pay/<oid>/', views.payable_invoice, name='invoice_pay'),
    path('order_status/<status>/', views.order_product_status, name='order_status'),
    
    # Stripe Connects
    path('authorize/', views.StripeAuthorizeView.as_view(), name='authorize'),
    path('oauth/callback/', views.StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),

    # Ajax
    path('mark-as-shipped/', views.mark_as_shipped, name='mark-as-shipped'),
    path('mark-as-arrived/', views.mark_as_arrived, name='mark-as-arrived'),
    path('mark-as-delivered/', views.mark_as_delivered, name='mark-as-delivered'),
    path('mark_as_seen/', views.mark_as_seen, name='mark_as_seen'),
    path('send_mail/', views.send_mail_func, name='send_mail'),
    
    path("shop/<vid>/", views.vendor_shop_view_page, name="vendor_shop_view_page"),
    path("notification/", views.vendor_notification, name="vendor_notification"),
    
    path("vendor_follow/", views.vendor_follow, name="vendor_follow"),
    path("vendor_follow-2/<id>", views.vendor_follow_2, name="vendor_follow_2"),
    
    # Coupon
    path("vendor-coupon/", views.vendor_coupon, name="vendor-coupon"),
    path("create_coupon/", views.create_coupon, name="create_coupon"),
    path("delete_coupon/<cid>/", views.delete_coupon, name="delete_coupon"),
    path("update_coupon/<cid>/", views.update_coupon, name="update_coupon"),
    
    # Messaging
    path('inbox/', views.inbox, name="inbox"),
    path('inbox/<username>/', views.get_inbox, name="inbox-detail"),
    # path('get_messages_ajax/<username>/', views.get_messages_ajax, name="get_messages_ajax"),
    path('send_message_ajax/<username>/', views.send_message_ajax, name="send_message_ajax"),
    path('search_user/', views.search_users, name="search_users"),
    
    # API Tests
    path('payout-view/', views.VendorPayoutView.as_view(), name='vendor-payout'),
    path('onboard_view_1/', views.onboard_seller_view, name='onboard_view_1'),
    path('onboard_seller_view_2/', views.onboard_seller_view_2, name='onboard_seller_view_2'),
    path('generate_paypal_access_token/', views.generate_paypal_access_token, name='generate_paypal_access_token'),
    

    
]