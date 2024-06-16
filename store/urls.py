from django.urls import path, include
from store import views

app_name = "store"



urlpatterns = [
    path("", views.index, name="home"),
    path("offer/", views.offer, name="offer"),
    path("category/", views.category_list, name="category"),
    path("shop/", views.shop, name="shop"),
    path("category/<str:meta_title>", views.category_shop, name="category-shop"),
    path("brand/<str:meta_title>", views.brand_shop, name="brand-shop"),
    path("hot_deals/", views.hot_deals, name="hot_deals"),
    path("search/", views.search_list, name="search"),
    path("my-cart/", views.cart_view, name="cart-view"),
    path("category/<cid>/", views.category_detail, name="category_detail"),
    path("shipping_address/", views.shipping_address, name="shipping_address"),
    path("checkout/<oid>/", views.checkout_view, name="checkout"),
    path("custom-checkout/<oid>/", views.custom_checkout_view, name="checkout2"),
    path('checkout/order-detail/<id>/', views.PaymentConfirmation.as_view(), name='order-detail'),
    path('success-payment/', views.PaymentSuccessView, name='success'),
    path('failed-payment/', views.PaymentFailedView, name='failed'),    
    
    path("payment-completed/<oid>/", views.payment_completed_view, name="payment-completed"),


    # Ajax URLs
    path("ajax/add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("ajax/helpful-review/", views.helpful_review, name="helpful-review"),
    path("ajax/add-review/<int:pid>/", views.add_review, name="add-review"),
    path("ajax/ask-question/", views.ask_question, name="ask-question"),
    path('ajax/update-cart/',views.update_cart,name='update-cart'),
    path('ajax/delete-from-cart/',views.delete_item_from_cart,name='delete-from-cart'),

    # API URLs
    path('api/checkout-session/<id>/', views.create_checkout_session, name='api_checkout_session'),
    path('country_get/', views.country_get, name='country_get'),


    path('webhook/', views.webhook, name='webhook'),



    path('get-subcategories/<str:category_meta_title>', views.get_subcategories, name='get-subcategories'),
    path('nav-search/', views.nav_search, name='nav-search'),
    path("<str:meta_title>/", views.product_detail, name="product-detail"),

]
