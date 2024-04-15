from addons.models import AboutUS, BasicAddon, Company, FAQs, Policy, SupportContactInformation, HomePageSetup, TaxRate, Home_Two, Home_One
from store import models
from django.contrib.gis.geoip2 import GeoIP2

from vendor.models import Vendor

def default(request):
    try:
        basic_addon = BasicAddon.objects.filter().first()
        payment_method = basic_addon.payment_method.all()
    except:
        basic_addon = None
        payment_method = None

        
    try:
        home_one_first = Home_One.objects.filter(active=True, first=True).first()
        home_one = Home_One.objects.filter(active=True, first=False)
    except:
        home_one = None
        home_one_first = None
    try:
        homepage = HomePageSetup.objects.all().first()
    except:
        homepage = None

    try:
        featured_products = models.Product.objects.filter(status="published", hero_section_featured=True)[:3]
        featured_products_2 = models.Product.objects.filter(status="published", hero_section_featured=True)[3:20]
        featured_hot_deals = models.Product.objects.filter(status="published", hot_deal=True)
    except:
        featured_products = None
        featured_hot_deals = None

    try:
        home_two = Home_Two.objects.filter(active=True)
    except:
        home_two = None
    
    try:
        basic_addon = BasicAddon.objects.filter().first()
        service_fee = basic_addon.service_fee_percentage / 100 
        service_fee_flat_rate = basic_addon.service_fee_flat_rate 
    except:
        basic_addon = None
        service_fee = 1
        service_fee_flat_rate = 1
    
    try:
        cs = basic_addon.currency_sign
    except:
        cs = "$"
    try:
        homepage_style = basic_addon.homepage_style
    except:
        homepage_style = None
    try:
        ca = basic_addon.currency_abbreviation
        
    except :
        ca = 'TND'
    try:
        signup_form = basic_addon.registration_form_type
    except:
        signup_form = None
    try:
        support_details = SupportContactInformation.objects.all().first()
    except:
        support_details = None
    try:
        faqs = FAQs.objects.filter(share=True)
    except:
        faqs = None
    try:
        vendor = request.user.vendor
    except:
        vendor = None
    try:
        all_vendors = Vendor.objects.filter(active=True).order_by("product_count")
    except:
        all_vendors = None
    try:
        category = models.Category.objects.filter(active=True)
    except:
        category = None
        
    try:
        brands = models.Brand.objects.filter(active=True)
    except:
        brands = None
        
    try:
        product_ = models.Product.objects.filter(status="published").order_by("-orders")
    except:
        product_ = None
    
    try:
        company = Company.objects.all().first()
    except:
        company = None
    try:
        policy = Policy.objects.all().first()
    except:
        policy = None

    try:
        about_us = AboutUS.objects.all().first()
    except:
        about_us = None
        
    try:
        # Country
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        g = GeoIP2()
        location = g.city(ip)
        location_country = location["country_name"]
        request.session['location_country'] = location_country
        tax_country = TaxRate.objects.filter(country=request.session['location_country']).first()
        tax = tax_country.rate / 100
        new_rate_ = tax_country.rate / 100
        # print("Session Country =====================", request.session['location_country'])
        # print("Session Rate =====================", new_rate_)
        
    except:
        location_country = "United States"
        request.session['location_country'] = location_country
        tax_country = TaxRate.objects.filter(country="Tunisia").first()
        tax = 0.2
        new_rate_ = 0.2
        
        # print("Session Country =====================", request.session['location_country'])
        # print("Session Rate =====================", new_rate_)
        
    # Service Fee Price
    
    try:
        support_details = SupportContactInformation.objects.all().first()
    except:
        support_details = None

    try:
        categories = models.Category.objects.all()
    except:
        categories = None

    try:
        service_fee_ = basic_addon.service_fee_percentage / 100 
        service_fee_flat_rate_ = basic_addon.service_fee_flat_rate
        service_fee_rate_ = 0
    except:
        service_fee_ = 0 / 100 
        service_fee_flat_rate_ = 0
        service_fee_rate_ = 0
    
    try:
        if basic_addon.service_fee_charge_type == "percentage":
            service_fee_rate_ = service_fee
            
        elif basic_addon.service_fee_charge_type == "flat_rate":
            service_fee_rate_ = service_fee_flat_rate
            
        else:
            service_fee_rate_ = 0.5
    except:
        if "flat_rate" == "percentage":
            service_fee_rate_ = service_fee

        elif "flat_rate" == "flat_rate":
            service_fee_rate_ = service_fee_flat_rate

        else:
            service_fee_rate_ = 0.5
    
    # print("Session Rate =====================", service_fee_rate_)
    
        
    cart_total_amount = 0
    tax_amount_ = 0
    shipping_amount = 0
    product_plus_shipping_session = 0
    service_fee_amount = 0
    total_session = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            shipping_amount += int(item['qty']) * float(item['shipping_amount'])
            product_plus_shipping_session = shipping_amount + cart_total_amount
            tax_amount_ = product_plus_shipping_session * tax
            
            service_fee_calc = cart_total_amount
            if basic_addon.service_fee_charge_type == "percentage":
                service_fee_amount = service_fee_calc * service_fee
                
            elif basic_addon.service_fee_charge_type == "flat_rate":
                service_fee_amount = service_fee_calc * float(service_fee_flat_rate)
                
            else:
                service_fee_amount = service_fee_calc * 0.5
                
            total_session = cart_total_amount + shipping_amount + tax_amount_ + service_fee_amount
            # print("total_session ==================", round(total_session, 2))
            # print("product_plus_shipping_session ==================", product_plus_shipping_session)
            # print("cart_total_amount ==================", cart_total_amount)
            # print("tax_amount_ ==================", tax_amount_)

    return {
        "signup_form": signup_form,
        "basic_addon": basic_addon,
        'cart_total_amount': cart_total_amount,
        "cs": cs,
        'vendor': vendor,
        "ca": ca,
        "home_one": home_one,
        "home_one_first": home_one_first,
        "homepage_style": homepage_style,
        "homepage": homepage,
        "home_two": home_two,
        "category": category,
        "company": company,
        "policy": policy,
        "about_us": about_us,
        'support_details': support_details,  # Add support_contact_info to the context
        'total_session': total_session,
        'faqs': faqs,
        'new_rate_': new_rate_,
        'service_fee_rate_': service_fee_rate_,
        "tax_country": tax_country,
        "brands": brands,
        "product_": product_,
        "all_vendors": all_vendors,
        "featured_products": featured_products,
        "featured_products_2": featured_products_2,
        "featured_hot_deals": featured_hot_deals,
        "payment_method": payment_method,
        "categories": categories,
    }