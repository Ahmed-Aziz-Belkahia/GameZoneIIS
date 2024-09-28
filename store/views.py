from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404 ,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound, JsonResponse
from django.db import models
from django.db.models import Min, Max
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q, Count, Sum, F, FloatField
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator
from django.core.mail import send_mail


from store.forms import CheckoutForm, ReviewForm
from store.models import RATING, CallToActionBanner, Genre, Mapping, Product, Category, CartOrder, CartOrderItem, Brand, Gallery, Review, ProductFaq, ProductBidders, ProductOffers, SubCategory, Type, brandMetaTitle, categoryMetaTitle, productMetaTitle, subcategoryMetaTitle
from core.models import Address
from blog.models import Post
from vendor.forms import CouponApplyForm
from vendor.models import Vendor, OrderTracker, PayoutTracker, Notification, Coupon
from addons.models import BasicAddon, Company, TaxRate

from datetime import datetime as d
from datetime import datetime
import datetime
import pytz
import json
import stripe
import requests
from decimal import Decimal
from anymail.message import attach_inline_image_file
from paypal.standard.forms import PayPalPaymentsForm


from fuzzywuzzy import fuzz
from fuzzywuzzy import process

utc=pytz.UTC

def index(request):
    """ addon = BasicAddon.objects.filter().first()
    brands = Brand.objects.filter(active=True)
    products = Product.objects.filter(status="published", featured=True).order_by("-id")[:10]
    top_selling_products = Product.objects.filter(status="published").order_by("-orders")[:10]
    hot_deal = Product.objects.filter(status="published", hot_deal=True).first()
    all_products = Product.objects.filter(status="published")[:16]
    posts = Post.objects.filter(status="published", featured=True)
    
    query = request.GET.get("q")
    if query:
        products = products.filter(Q(title__icontains=query)|Q(description__icontains=query)).distinct()
        
    
    
    context = {
        "all_products":all_products,
        "addon":addon,
        "posts":posts,
        "brands":brands,
        'hot_deal':hot_deal,
        "products":products,
        "top_selling_products":top_selling_products,
    }
    #return render(request, "store/index.html", context) """
    import logging

    logger = logging.getLogger('django')

    def test_logging(request):
        logger.debug('Debug message')
        return HttpResponse('Logging Test')
    heros = Product.objects.filter(hero_section_featured=True)
    top_deals = Product.objects.filter(deal_category="top_deal")
    top_deals_banner = CallToActionBanner.objects.filter(CTA_type="top_deal").first()
    pre_owned_deals = Product.objects.filter(deal_category="pre_owned")
    pre_owned_deals_banner = CallToActionBanner.objects.filter(CTA_type="pre_owned").first()
    cta1 = CallToActionBanner.objects.filter(CTA_type="first").first()
    cta2 = CallToActionBanner.objects.filter(CTA_type="second").first()
    cta3 = CallToActionBanner.objects.filter(CTA_type="third").first()
    cta4 = CallToActionBanner.objects.filter(CTA_type="forth").first()
    top_hardware = Product.objects.filter(catalog_type="top_hardware")
    top_accessories = Product.objects.filter(catalog_type="top_accessories")
    top_games = Product.objects.filter(catalog_type="top_games")
    brands = Brand.objects.filter(featured=True, active=True)
    playstation_deals = Product.objects.filter(deal_category="playstation")
    playstation_banner = CallToActionBanner.objects.filter(CTA_type="playstation").first()
    nintendo_deals = Product.objects.filter(deal_category="nintendo")
    nintendo_banner = CallToActionBanner.objects.filter(CTA_type="nintendo").first()
    featured_games = Product.objects.filter(featured_game=True, game=True)
    featured_games_sliders = Product.objects.filter(add_to_featured_games_slider=True)
    featured_genres = Genre.objects.filter(featured=True, active=True)

    context = {
        'heros':                    heros,
        'top_deals':                top_deals,
        'top_deals_banner':         top_deals_banner,
        'pre_owned_deals':          pre_owned_deals,
        'pre_owned_deals_banner':   pre_owned_deals_banner,
        'cta1':                     cta1,
        'cta2':                     cta2,
        'cta3':                     cta3,
        'cta4':                     cta4,
        'top_hardware':             top_hardware,
        'top_accessories':          top_accessories,
        'top_games':                top_games,
        'brands':                   brands,
        'playstation_deals':        playstation_deals,
        'playstation_banner':       playstation_banner,
        'nintendo_deals':           nintendo_deals,
        'nintendo_banner':          nintendo_banner,
        'featured_games':           featured_games,
        'featured_games_sliders':   featured_games_sliders,
        'featured_genres':          featured_genres,
    }
    return render(request, "gz/home.html", context)

def get_subcategories(request, category_meta_title):
    try:
        # Filter subcategories under the given category without a parent subcategory
        subcategories = SubCategory.objects.filter(category__meta_title=category_meta_title, parent_subcategory__isnull=True)
        
        # Manually construct a list of dictionaries from the queryset
        subcategories_list = []
        for subcategory in subcategories:
            subcategory_dict = {
                'meta_title': subcategory.meta_title,
                'title': subcategory.title,
                'full_p': subcategory.get_full_path_with_slashes()
                # Add more fields if needed
            }
            subcategories_list.append(subcategory_dict)
        
        # Return the list of dictionaries as JsonResponse
        return JsonResponse({"success": True, 'subcategories': subcategories_list})
    except SubCategory.DoesNotExist:
        # Handle the case where no subcategories are found for the given category ID
        # You might want to render an appropriate error page or handle it in another way
        return JsonResponse({"success": True, 'subcategories': None})



def category_list(request):
    categories_ = Category.objects.filter(active=True)
    
    context = {
        "categories_":categories_,
    }
    return render(request, "store/categories.html", context)


def get_fuzzy_matched_products(query, products, threshold=70):
    product_data = [
        (product.id, product.title or "", product.brand.title or "", product.category.title or "")
        for product in products
    ]

    def match_score(product):
        title_score = fuzz.partial_ratio(query, product[1])
        brand_score = fuzz.partial_ratio(query, product[2])
        return max(title_score, brand_score)

    matched_product_ids = [product[0] for product in product_data if match_score(product) >= threshold]
    return products.filter(id__in=matched_product_ids).distinct()

def get_mapped_query(query):
    mapping = Mapping.objects.filter(key=query).first()
    return mapping.value if mapping else query

def search_list(request):
    query = request.GET.get("q")
    
    if query:
        query = get_mapped_query(query.lower())

    products = Product.objects.filter(status="published").order_by("index")

    if query:
        products = get_fuzzy_matched_products(query, products)

    product_count = products.count()

    paginator = Paginator(products, 16)  # 16 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        "product_count": product_count,
        "products": products,
        "query": query,
    }
    return render(request, "store/search_list.html", context)

def nav_search(request):
    if request.method == 'POST':
        query = request.POST.get("q")
        
        if query:
            query = get_mapped_query(query.lower())
            print(query)

        products = Product.objects.filter(status="published").order_by("index")

        if query:
            products = get_fuzzy_matched_products(query, products)

        product_count = products.count()

        paginator = Paginator(products, 16)
        page_number = request.POST.get('page') or 1
        products = paginator.get_page(page_number)

        query_list = [{'meta_title': product.meta_title, 'title': product.title} for product in products.object_list]

        context = {
            "success": True,
            "product_count": product_count,
            "query": query,
            "query_list": query_list,
        }
        return JsonResponse(context)

    return JsonResponse({'success': False, 'queryList': []})
def shop(request):
    products = Product.objects.filter(status="published").order_by("index")
    filtered_products = products
    products_count = products.count()
    top_selling = Product.objects.filter(status="published").order_by("-orders")[:20]

    # Get all categories, brands, and subcategories associated with the products
    categories = Category.objects.filter(products__in=products).distinct()
    brands = Brand.objects.filter(product_brand__in=products).distinct()
    direct_subcategories = SubCategory.objects.none()

    q = request.GET.get('q')
    
    if q:
        q = get_mapped_query(q.lower())
    
    if q:
        filtered_products = filtered_products.filter(title__icontains=q) | filtered_products.filter(description__icontains=q)

    print(f"Initial product count: {products.count()}")
    if q:
        print(f"Product count after fuzzy matching: {filtered_products.count()}")
        matched_ids = filtered_products.values_list('id', flat=True)
        print(f"Matched product IDs: {list(matched_ids)}")

    for category in categories:
        direct_subcategories = direct_subcategories.union(category.subcategories.filter(parent_subcategory=None))

    # Filter products by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if not min_price:
        min_price = filtered_products.aggregate(min_price=Min('price'))['min_price']

    if not max_price:
        max_price = filtered_products.aggregate(max_price=Max('price'))['max_price']

    if min_price and max_price:
        filtered_products = filtered_products.filter(price__range=(min_price, max_price))
    
    # Filter products by selected categories
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        filtered_products = filtered_products.filter(category__meta_title__in=selected_categories)

    # Filter products by selected subcategories
    selected_subcategories = request.GET.getlist('subcategories')
    if selected_subcategories:
        filtered_products = filtered_products.filter(category__subcategories__meta_title__in=selected_subcategories)

    # Filter products by selected brands
    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        filtered_products = filtered_products.filter(brand__meta_title__in=selected_brands)

    # Step 1: Get all reviews from products
    all_reviews = Review.objects.filter(product__in=products)
    
    # Step 2: Extract the ratings from these reviews
    all_ratings = [review.rating for review in all_reviews]
    
    # Step 3: Remove duplicate ratings
    unique_ratings = sorted(set(all_ratings))
    
    # Filter products by selected ratings
    selected_ratings = [int(rating.strip()) for rating in request.GET.getlist('ratings')]
    if selected_ratings:
        filtered_products = filtered_products.filter(reviews__rating__in=selected_ratings).distinct()

    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'price-low-to-high':
            filtered_products = filtered_products.order_by("index", 'price')
        elif sort_by == 'price-high-to-low':
            filtered_products = filtered_products.order_by("index", '-price')

    # Paginate the filtered products
    paginator = Paginator(filtered_products, 16)
    page_number = request.GET.get('page')
    pages_filtered_products = paginator.get_page(page_number)

    context = {
        "direct_subcategories": direct_subcategories,
        "shop_categories": categories,
        "brands": brands,
        "products_count": products_count,
        "products": pages_filtered_products,
        "top_selling": top_selling,
        "min_price": min_price,
        "max_price": max_price,
        'all_ratings': [(rating, '★' * rating + '☆' * (5 - rating)) for rating in unique_ratings],
        'selected_categories': selected_categories,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'selected_ratings': selected_ratings,
    }
    return render(request, "store/shop.html", context)


def category_shop(request, meta_title):
    try:
        category = Category.objects.get(meta_title=meta_title)
    except:
        category_meta_title = categoryMetaTitle.objects.filter(meta_title=meta_title).first()
        if category_meta_title:
            return redirect('store:category-shop', meta_title=category_meta_title.category.meta_title, permanent = True)
        else:
            return redirect("404")


    products = Product.objects.filter(category__meta_title__in=[category.meta_title], status="published").order_by('index')
    brands = Brand.objects.filter(active=True)
    filtered_products = products
    products_count = products.count()
    top_selling = Product.objects.filter(category__meta_title__in=[meta_title], status="published").order_by("index", "-orders")[:20]
    query_params = request.GET
    # Filter
    # Get category object
    # Get direct subcategories objects
    direct_subcategories = category.subcategories.filter(parent_subcategory=None)
    # Get brands associated with the products
    brands = Brand.objects.filter(product_brand__in=products).distinct()


    q=request.GET.get('q')
    if q:
        filtered_products = filtered_products.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(category__title__icontains=q)).distinct()


    # Filter products by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if not min_price:
        min_price = filtered_products.aggregate(min_price=Min('price'))['min_price']

    if not max_price:
        max_price = filtered_products.aggregate(max_price=Max('price'))['max_price']

    # Filter products by price range
    if min_price and max_price:
        filtered_products = filtered_products.filter(price__range=(min_price, max_price))
    
    # Filter products by selected direct subcategories
    selected_subcategories = request.GET.getlist('subcategories')


    sc = None
    if selected_subcategories:
        if len(selected_subcategories) == 1:
            sc = SubCategory.objects.get(meta_title=selected_subcategories[0])
        filtered_products = filtered_products.filter(subcategory__meta_title__in=selected_subcategories)


    # Filter products by selected brands
    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        filtered_products = filtered_products.filter(brand__meta_title__in=selected_brands)

    # Step 1: Get all reviews from products
    all_reviews = Review.objects.filter(product__in=products)
    
    # Step 2: Extract the ratings from these reviews
    all_ratings = [review.rating for review in all_reviews]
    
    # Step 3: Remove duplicate ratings
    unique_ratings = sorted(set(all_ratings))
    
    # Filter products by selected ratings
    selected_ratings = [int(rating.strip()) for rating in request.GET.getlist('ratings')]
    if selected_ratings:
        filtered_products = filtered_products.filter(reviews__rating__in=selected_ratings).distinct()

    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'price-low-to-high':
            filtered_products = filtered_products.order_by("index", 'price')
        elif sort_by == 'price-high-to-low':
            filtered_products = filtered_products.order_by("index", '-price')    

    # Paginate the filtered products
    paginator = Paginator(filtered_products, 16)
    page_number = request.GET.get('page')
    pages_filtered_products = paginator.get_page(page_number)

    context = {
        "current_category": category,
        "direct_subcategories": direct_subcategories,
        "brands": brands,
        "products_count": products_count,
        "products": pages_filtered_products,
        "top_selling": top_selling,
        "min_price": min_price,
        "max_price": max_price,
        'all_ratings': [(rating, '★' * rating + '☆' * (5 - rating)) for rating in unique_ratings],
        'selected_ratings': selected_ratings,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'sc': sc,
    }
    if products:
        return render(request, "store/category_shop.html", context)
    else:
       return redirect(reverse("store:home"))
    


def subcategory_shop(request, category_meta_title, subcategory_path):
    r1=False
    r2=False
    try:
        category = Category.objects.get(meta_title=category_meta_title)
    except:
        category_meta_title_obj = categoryMetaTitle.objects.filter(meta_title=category_meta_title).first()
        if category_meta_title_obj:
            r1=True
        # else:
        #     return redirect("404")
        



    # Split the subcategory path by "/"
    subcategory_meta_titles = subcategory_path.split('/')
    print(subcategory_meta_titles)
    print("Category Meta Title:", category_meta_title)
    print("Subcategory Meta Titles:", subcategory_meta_titles)
    
    # Assuming that the last element in subcategory_meta_titles is the current subcategory
    current_subcategory_meta_title = subcategory_meta_titles[-1]
    try:
        subcategory = SubCategory.objects.get(meta_title=current_subcategory_meta_title)
    except:
        print(subcategoryMetaTitle.objects.all(), "-----------------------------------------------")
        print(current_subcategory_meta_title, "-----------------------------------------------")
        print(subcategoryMetaTitle.objects.filter(meta_title=current_subcategory_meta_title))
        subcategory_meta_title = subcategoryMetaTitle.objects.filter(meta_title=current_subcategory_meta_title).first()
        if subcategory_meta_title:
            r2=True
        # else:
        #     return redirect("404")


    # if r1  and r2:
    #     return redirect('store:subcategory-shop', category_meta_title=category_meta_title_obj.category.meta_title, subcategory_path=subcategory_meta_title.subcategory.get_full_path_with_slashes(), permanent = True)
    # if r1:
    #     return redirect('store:subcategory-shop', category_meta_title=category_meta_title_obj.category.meta_title, subcategory_path=subcategory_path, permanent = True)
    # if r2:
    #     return redirect('store:subcategory-shop', category_meta_title=category_meta_title, subcategory_path=subcategory_meta_title.subcategory.get_full_path_with_slashes(), permanent = True)

    products = Product.objects.filter(subcategory__meta_title__in=[subcategory.meta_title], status="published").order_by('index')
    brands = Brand.objects.filter(active=True)
    filtered_products = products
    products_count = products.count()
    top_selling = Product.objects.filter(category__meta_title__in=[current_subcategory_meta_title], status="published").order_by("index", "-orders")[:20]
    query_params = request.GET
    # Filter
    # Get category object
    # Get direct subcategories objects
    # Get brands associated with the products
    brands = Brand.objects.filter(product_brand__in=products).distinct()


    q=request.GET.get('q')
    if q:
        filtered_products = filtered_products.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(category__title__icontains=q)).distinct()


    # Filter products by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if not min_price:
        min_price = filtered_products.aggregate(min_price=Min('price'))['min_price']

    if not max_price:
        max_price = filtered_products.aggregate(max_price=Max('price'))['max_price']

    # Filter products by price range
    if min_price and max_price:
        filtered_products = filtered_products.filter(price__range=(min_price, max_price))
    
    # Filter products by selected direct subcategories
    selected_subcategories = request.GET.getlist('subcategories')


    sc = None
    if selected_subcategories:
        if len(selected_subcategories) == 1:
            sc = SubCategory.objects.get(meta_title=selected_subcategories[0])
        filtered_products = filtered_products.filter(subcategory__meta_title__in=selected_subcategories)


    # Filter products by selected brands
    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        filtered_products = filtered_products.filter(brand__meta_title__in=selected_brands)

    # Step 1: Get all reviews from products
    all_reviews = Review.objects.filter(product__in=products)
    
    # Step 2: Extract the ratings from these reviews
    all_ratings = [review.rating for review in all_reviews]
    
    # Step 3: Remove duplicate ratings
    unique_ratings = sorted(set(all_ratings))
    
    # Filter products by selected ratings
    selected_ratings = [int(rating.strip()) for rating in request.GET.getlist('ratings')]
    if selected_ratings:
        filtered_products = filtered_products.filter(reviews__rating__in=selected_ratings).distinct()

    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'price-low-to-high':
            filtered_products = filtered_products.order_by("index", 'price')
        elif sort_by == 'price-high-to-low':
            filtered_products = filtered_products.order_by("index", '-price')    

    # Paginate the filtered products
    paginator = Paginator(filtered_products, 16)
    page_number = request.GET.get('page')
    pages_filtered_products = paginator.get_page(page_number)

    context = {
        "current_subcategory": subcategory,
        "brands": brands,
        "products_count": products_count,
        "products": pages_filtered_products,
        "top_selling": top_selling,
        "min_price": min_price,
        "max_price": max_price,
        'all_ratings': [(rating, '★' * rating + '☆' * (5 - rating)) for rating in unique_ratings],
        'selected_ratings': selected_ratings,
        'selected_subcategories': selected_subcategories,
        'selected_brands': selected_brands,
        'sc': sc,
    }
    if products:
        return render(request, "store/subcategory_shop.html", context)
    else:
       return redirect(reverse("store:home"))


def brand_shop(request, meta_title):
    try:
        brand = Brand.objects.get(meta_title=meta_title)
    except:
        brand_meta_title = brandMetaTitle.objects.filter(meta_title=meta_title).first()
        if brand_meta_title:
            return redirect('store:brand-shop', meta_title=brand_meta_title.brand.meta_title, permanent = True)
        else:
            return redirect("404")
    products = Product.objects.filter(brand=brand, status="published").order_by("index")
    filtered_products = products
    products_count = products.count()
    top_selling = Product.objects.filter(brand=brand, status="published").order_by("index", "-orders")[:20]
    query_params = request.GET

    # Get category object
    categories = Category.objects.filter(products__in=products).distinct()

    q=request.GET.get('q')
    if q:
        filtered_products = filtered_products.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(category__title__icontains=q)).distinct()



    # Get all categories and filter products by selected categories
    selected_categories = request.GET.getlist('categories')
    if selected_categories:
        filtered_products = filtered_products.filter(category__meta_title__in=selected_categories)

    # Get direct subcategories objects
    direct_subcategories = []
    for category in categories:
        direct_subcategories.extend(category.subcategories.filter(parent_subcategory=None))

    # Get brands associated with the products
    # Filter products by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if not min_price:
        min_price = filtered_products.aggregate(min_price=Min('price'))['min_price']

    if not max_price:
        max_price = filtered_products.aggregate(max_price=Max('price'))['max_price']

    # Filter products by price range
    if min_price and max_price:
        filtered_products = filtered_products.filter(price__range=(min_price, max_price))
    
    # Filter products by selected direct subcategories
    selected_subcategories = request.GET.getlist('subcategories')
    if selected_subcategories:
        filtered_products = filtered_products.filter(subcategory__meta_title__in=selected_subcategories)

    # Step 1: Get all reviews from products
    all_reviews = Review.objects.filter(product__in=products)
    
    # Step 2: Extract the ratings from these reviews
    all_ratings = [review.rating for review in all_reviews]
    
    # Step 3: Remove duplicate ratings
    unique_ratings = sorted(set(all_ratings))
    
    # Filter products by selected ratings
    selected_ratings = [int(rating.strip()) for rating in request.GET.getlist('ratings')]
    if selected_ratings:
        filtered_products = filtered_products.filter(reviews__rating__in=selected_ratings).distinct()

    sort_by = request.GET.get('sort_by')
    if sort_by:
        if sort_by == 'price-low-to-high':
            filtered_products = filtered_products.order_by("index", 'price')
        elif sort_by == 'price-high-to-low':
            filtered_products = filtered_products.order_by("index", '-price')  

    # Paginate the filtered products
    paginator = Paginator(filtered_products, 16)
    page_number = request.GET.get('page')
    pages_filtered_products = paginator.get_page(page_number)

    context = {
        "brand": brand,
        "direct_subcategories": direct_subcategories,
        "shop_categories": categories,
        "products_count": products_count,
        "products": pages_filtered_products,
        "top_selling": top_selling,
        "min_price": min_price,
        "max_price": max_price,
        'all_ratings': [(rating, '★' * rating + '☆' * (5 - rating)) for rating in unique_ratings],
        'selected_ratings': selected_ratings,
        'selected_categories': selected_categories,
        'selected_subcategories': selected_subcategories,
    }
    if products:
        return render(request, "store/brand_shop.html", context)
    else:
       return redirect(reverse("store:home"))


def hot_deals(request):
    products = Product.objects.filter(status="published", hot_deal=True).order_by("index")
    
    query = request.GET.get("q")
    if query:
        products = products.filter(Q(title__icontains=query)|Q(description__icontains=query)).distinct()
    
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products":products,
    }
    return render(request, "store/hot-deals.html", context)



def category_detail(request, cid):
    category__ = Category.objects.get(cid=cid)
    top_selling = Product.objects.filter(status="published", category=category__).order_by("index")[:10]
    products = Product.objects.filter(status="published", category=category__).order_by("index", "orders")
    
    
    context = {
        "category__":category__,
        "products":products,
        "top_selling":top_selling,
    }
    return render(request, "store/category-detail.html", context)

def auction(request):
    products = Product.objects.filter(status="published", type="auction").order_by("index")
    products_count = Product.objects.filter(status="published", type="auction")
    
    query = request.GET.get("q")
    if query:
        products = products.filter(Q(title__icontains=query)|Q(description__icontains=query)).distinct()
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        "products":products,
        "products_count":products_count,
    }
    return render(request, "store/auction.html", context)

@login_required
def auction_detail(request, pid):
    product = Product.objects.get(status="published", type="auction", pid=pid)
    bidders = ProductBidders.objects.filter(product=product, active=True).order_by("-price")[:3]
    other_bidders = ProductBidders.objects.filter(product=product, active=True).order_by("-price")
    message = ""
    alert_tag = "success"
    completed = False
    winner = ProductBidders.objects.filter(product=product, active=True).order_by("-price").first()
    
    
    if timezone.now() < product.ending_date:
        message = "Bidding is still on going."
        completed = False
        product.auction_status = "on_going"
        product.bidding_ended = False
        product.save()
        try:
            winner.winner = False
            winner.win_status = "pending"
            winner.save()
        except:
            pass
        ProductBidders.objects.filter(product=product).update(winner=False)
        
    else:
        message = "Bidding have been completed"
        product.auction_status = "finished"
        product.bidding_ended = True
        product.save()
        completed = True
        try:
            winner.winner = True
            winner.win_status = "won"
            winner.save()
        except:
            pass
    
    if request.method == "POST":
        price = request.POST.get("price")
        if Decimal(price) < product.price:
            messages.warning(request, "You bidding price cannot be lower than the starting price")
            return redirect("store:auction_detail", product.pid)
        
        ProductBidders.objects.create(
            user=request.user,
            product=product,
            price=price,
            email=request.user.email,
            active=True
        )
        product.bidders.add(request.user)
        product.save()
        messages.success(request, "Bidding Placed Successfully.")
        return redirect("store:auction_detail", product.pid)
    
    context = {
        "winner":winner,
        "completed":completed,
        "alert_tag":alert_tag,
        "message":message,
        "product":product,
        "bidders":bidders,
        "other_bidders":other_bidders,
    }
    return render(request, "store/auction_detail.html", context)

@login_required
def auction_update(request, pid, bid):
    product = Product.objects.get(status="published", type="auction", pid=pid)
    bidders = ProductBidders.objects.filter(product=product, active=True).order_by("-price")[:3]
    other_bidders = ProductBidders.objects.filter(product=product, active=True).order_by("-price")
    bidding = ProductBidders.objects.get(bid=bid, product=product)
    
    if timezone.now() > product.ending_date:
        messages.error(request, "Bidding have been concluded, you cannot update your bidding amout again.")
        return redirect("store:auction_detail", product.pid)
    
    if request.method == "POST":
        price = request.POST.get("price")
        if Decimal(price) < product.price:
            messages.warning(request, "You bidding price cannot be lower than the starting price")
            return redirect("store:auction_update", product.pid, bidding.bid)
        
        if Decimal(price) < bidding.price:
            messages.warning(request, "You cannot go lower than your current bidding price")
            return redirect("store:auction_update", product.pid, bidding.bid)
        
        if Decimal(price) == bidding.price:
            messages.warning(request, "Your current bidding price cannot be the same as the new bidding price")
            return redirect("store:auction_update", product.pid, bidding.bid)
        
        
        bidding.price = Decimal(price)
        bidding.save()
        messages.success(request, "Bidding Placed Successfully.")
        return redirect("store:auction_detail", product.pid)
    
    context = {
        "product":product,
        "bidders":bidders,
        "other_bidders":other_bidders,
    }
    return render(request, "store/auction_update.html", context)


def offer(request):
    brands = Brand.objects.filter(active=True)
    products = Product.objects.filter(status="published", type="offer")

    context = {
        "brands":brands,
        "products":products,
    }
    return render(request, "store/offer.html", context)

def product_detail(request, meta_title):

    try:
        product = Product.objects.get(meta_title=meta_title)
    except:
        product_meta_title = productMetaTitle.objects.filter(meta_title=meta_title).first()
        if product_meta_title:
            return redirect('store:product-detail', meta_title=product_meta_title.product.meta_title, permanent = True)
        else:
            return redirect("404")

    try:
        product = Product.objects.get(status="published", meta_title=meta_title)
    except Product.DoesNotExist:
        return redirect('404')
    disable_button = False
    if product.stock_qty == 0:
        disable_button = True
    
    if product.status == "disabled":
        return redirect("store:home")
    
    product_images = Gallery.objects.filter(product=product)
    vendor = Vendor.objects.get(user=product.user)
    vendor_product = Product.objects.filter(vendor=vendor).order_by("index")
    reviews = Review.objects.filter(product=product, active=True).order_by("-id")
    review_form = ReviewForm()

    five_star = Review.objects.filter(product=product, active=True, rating=5).count()
    four_star = Review.objects.filter(product=product, active=True, rating=4).count()
    three_star = Review.objects.filter(product=product, active=True, rating=3).count()
    two_star = Review.objects.filter(product=product, active=True, rating=2).count()
    one_star = Review.objects.filter(product=product, active=True, rating=1).count()

    relatedproduct = None  # Initialize relatedproduct outside the loop
    
    
    relatedproduct = Product.objects.filter(category=product.category, status="published").order_by("index")[:5]
    # Exit the loop after finding related products for the first category
    
    youmightlike = Product.objects.filter(status="published").order_by("index", "orders")[:5]
    
    questions_answers = ProductFaq.objects.filter(product=product, active=True).order_by("-id")
    
    # Bdding
    bidders = ProductBidders.objects.filter(product=product).order_by("-price")[:3]
    all_bidders = ProductBidders.objects.filter(product=product).order_by("-price")
    basic_addon = BasicAddon.objects.all().first()
    
    # Handlers
    make_review = True 
    make_bid = True 
    make_offer = True 
    reviewer_status = False
    if request.user.is_authenticated:
        all_orders = CartOrder.objects.filter(buyer=request.user, payment_status="paid")
        
        if all_orders.exists():
            reviewer_status = True
        else:
            reviewer_status = False
        
   
    service_fee = basic_addon.service_fee_percentage / 100 
    service_fee_flat_rate = basic_addon.service_fee_flat_rate
    service_fee_rate = 0
    
    if basic_addon.service_fee_charge_type == "percentage":
        processing_fee = float(product.price) * float(service_fee)
        service_fee_rate = service_fee
        
    elif basic_addon.service_fee_charge_type == "flat_rate":
        processing_fee = float(product.price) * float(service_fee_flat_rate)
        service_fee_rate = service_fee_flat_rate
        
        
    else:
        processing_fee = float(product.price) * 0.5
        service_fee_rate = 0
        
        
    location_country = "Tunisia"
    
    tax = TaxRate.objects.filter(country=location_country, active=True).first()
    if tax:
        new_rate = tax.rate / 100
    else:
        new_rate = 0.22
    product_plus_shipping = product.price + product.shipping_amount
    tax_rate_amount = Decimal(new_rate) * product_plus_shipping
    
    # print("tax_rate_amount  =====================", round(tax_rate_amount, 2))
    # print("tax_rate_amount  =====================", round(tax_rate_amount, 2))
    # print("tax_rate_amount  =====================", round(tax_rate_amount, 2))
    
    total_price = product.price + Decimal(tax_rate_amount) + Decimal(processing_fee) + Decimal(product.shipping_amount)
    
    
    try:
        my_bid_obj = ProductBidders.objects.filter(product=product, user=request.user).first()
        my_bid = ProductBidders.objects.filter(product=product, user=request.user)
    except:
        my_bid = None
        my_bid_obj = None
        
        
    try:
        my_offer_obj = ProductOffers.objects.filter(product=product, user=request.user).first()
        my_offer = ProductOffers.objects.filter(product=product, user=request.user)
        if my_offer.exists():
            make_offer = False
    except:
        my_offer = None
        my_offer_obj = None
    

    if request.user.is_authenticated:
        user_review_count = Review.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False
    
    if request.user.is_authenticated:
        if product.type == "offer":
            try:
                my_offer_obj = ProductOffers.objects.filter(product=product, user=request.user).first()
                my_offer = ProductOffers.objects.filter(product=product, user=request.user)
                if my_offer.exists():
                    make_offer = False
            except:
                my_offer = None
                my_offer_obj = None
                
            if make_offer == True:
                if request.method == "POST":
                    amount = request.POST.get("offer_amount")
                    message = request.POST.get("custom_message")
                    
                    
                    offer = ProductOffers.objects.create(user=request.user,price=amount,message=message,product=product,email=request.user.email)
                    Notification.objects.create(vendor=product.vendor,product=product,offer=offer,amount=amount,type="new_offer")
                    basic_addon = BasicAddon.objects.all().first()
                    if basic_addon.send_email_notifications == True:
                    
                        company = Company.objects.all().first()
                        merge_data = {
                            'company': company, 
                            'o': product, 
                        }
                        subject = f"New Offer for {product.title}"
                        text_body = render_to_string("email/message_body.txt", merge_data)
                        html_body = render_to_string("email/message_offer.html", merge_data)
                        
                        msg = EmailMultiAlternatives(
                            subject=subject, from_email=settings.FROM_EMAIL,
                            to=[product.vendor.shop_email], body=text_body
                        )
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()
                    messages.success(request, f"Offer submitted successfully.")
                    return redirect("store:product-detail", product.meta_title)

            if make_offer == False:
                if request.method == "POST":
                    price = request.POST.get("offer_amount_update")
                    my_offer_obj.price = price
                    my_offer_obj.save()
                    messages.success(request, "Offer Updated Successfully.")
                    
                    # Email ======================
                    basic_addon = BasicAddon.objects.all().first()
                    if basic_addon.send_email_notifications == True:
                        company = Company.objects.all().first()
                        merge_data = {
                            'company': company, 
                            'o': product, 
                            'bid': winner, 
                        }
                        subject = f"Updated Offer Price for {product.title}"
                        text_body = render_to_string("email/message_body.txt", merge_data)
                        html_body = render_to_string("email/message_offer.html", merge_data)
                        
                        msg = EmailMultiAlternatives(
                            subject=subject, from_email=settings.FROM_EMAIL,
                            to=[product.vendor.shop_email], body=text_body
                        )
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()
                        # Email ==========================
                    
                    return redirect("store:product-detail", product.meta_title)
                
    if request.user.is_authenticated:
        if product.type == "auction":
            winner = ProductBidders.objects.filter(product=product, active=True).order_by("-price").first()
            try:
                my_bid_obj = ProductBidders.objects.filter(product=product, user=request.user).first()
                my_bid = ProductBidders.objects.filter(product=product, user=request.user)
                # print("my bid =======================", my_bid_obj.price)
                # print("my bid Exist =======================", my_bid.exists())
                if my_bid.exists():
                    make_bid = False
            except:
                my_bid = None
                my_bid_obj = None
            
            if timezone.now() < product.ending_date:
                message = "Bidding is still on going."
                completed = False
                product.auction_status = "on_going"
                product.bidding_ended = False
                product.save()
                try:
                    winner.winner = False
                    winner.win_status = "pending"
                    winner.save()
                except:
                    pass
                ProductBidders.objects.filter(product=product).update(winner=False)
                
            else:
                message = "Bidding have been completed"
                product.auction_status = "finished"
                product.bidding_ended = True
                product.save()
                completed = True
                try:
                    winner.winner = True
                    winner.win_status = "won"
                    winner.save()
                except:
                    pass
            if make_bid == True:
                if request.method == "POST":
                    price = request.POST.get("bidding_amount")
                    if Decimal(price) < product.price:
                        messages.warning(request, "You bidding price cannot be lower than the starting price")
                        return redirect("store:product-detail", product.meta_title)
                    
                    bid = ProductBidders.objects.create(
                        user=request.user,
                        product=product,
                        price=price,
                        email=request.user.email,
                        active=True
                    )
                    product.bidders.add(request.user)
                    product.save()
                    Notification.objects.create(
                        vendor=product.vendor,
                        product=product,
                        bid=bid,
                        amount=price,
                        type="new_bidding"
                )
                    messages.success(request, "Bidding Placed Successfully.")
                    
                    # Email ======================
                    basic_addon = BasicAddon.objects.all().first()
                    if basic_addon.send_email_notifications == True:
                    
                        company = Company.objects.all().first()
                        merge_data = {
                            'company': company, 
                            'o': product, 
                            'bid': winner, 
                        }
                        subject = f"New Bidding for {product.title}"
                        text_body = render_to_string("email/message_body.txt", merge_data)
                        html_body = render_to_string("email/message_bidding.html", merge_data)
                        
                        msg = EmailMultiAlternatives(
                            subject=subject, from_email=settings.FROM_EMAIL,
                            to=[product.vendor.shop_email], body=text_body
                        )
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()
                    # Email ==========================
                    
                    return redirect("store:product-detail", product.meta_title)
                
            if make_bid == False:
                if request.method == "POST":
                    price = request.POST.get("bidding_amount_update")
                    if Decimal(price) < my_bid_obj.price:
                        messages.warning(request, "You New bidding price cannot be lower than your previous price")
                        return redirect("store:product-detail", product.meta_title)
                    
                    my_bid_obj.price = price
                    my_bid_obj.save()
                    messages.success(request, "Bidding Updated Successfully.")
                    
                    # Email ======================
                    basic_addon = BasicAddon.objects.all().first()
                    if basic_addon.send_email_notifications == True:
                        company = Company.objects.all().first()
                        merge_data = {
                            'company': company, 
                            'o': product, 
                            'bid': winner, 
                        }
                        subject = f"Updated Bidding Price for {product.title}"
                        text_body = render_to_string("email/message_body.txt", merge_data)
                        html_body = render_to_string("email/message_bidding_updated.html", merge_data)
                        
                        msg = EmailMultiAlternatives(
                            subject=subject, from_email=settings.FROM_EMAIL,
                            to=[product.vendor.shop_email], body=text_body
                        )
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()
                        # Email ==========================
                    
                    return redirect("store:product-detail", product.meta_title)

    context = {
        "disable_button": disable_button,
        "bidders":bidders,
        "product":product,
        "product_images":product_images,
        "vendor":vendor,
        "vendor_product":vendor_product,
        "reviews":reviews,
        "review_form":review_form,
        "tax_rate_amount":tax_rate_amount,
        "tax":tax,
        "processing_fee":processing_fee,
        # Handlers
        "make_review":make_review,
        "make_bid":make_bid,
        "my_bid":my_bid,
        "my_bid_obj":my_bid_obj,
        "all_bidders":all_bidders,
        # Offers
        "my_offer":my_offer,
        "my_offer_obj":my_offer_obj,
        "make_offer":make_offer,
        # Star ratings
        "five_star":five_star,
        "four_star":four_star,
        "three_star":three_star,
        "two_star":two_star,
        "one_star":one_star,
        "questions_answers":questions_answers,
        "relatedproduct":relatedproduct,
        "youmightlike":youmightlike,
        "questions_answers":questions_answers,
        "total_price":total_price,
        "new_rate":new_rate,
        "service_fee_rate":service_fee_rate,
        "reviewer_status":reviewer_status,
    }
    return render(request, "store/product_detail.html", context)


def helpful_review(request):
    print("helpful")
    id = request.GET['id']
    review = Review.objects.get(id=id)
    if request.user in review.helpful.all():
        review.helpful.remove(request.user)
        review.save()

    else:
        review.helpful.add(request.user)
        review.save()

    data = {
        "bool": True,
        "message": "Thanks for rating this review"
    }
    return JsonResponse({"data":data})

def add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user 

    review = Review.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_reviews = Review.objects.filter(product=product).aggregate(rating=models.Avg("rating"))

    return JsonResponse(
       {
        'bool': True,
        'context': context,
        'average_reviews': average_reviews
       }
    )


def ask_question(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    faq = ProductFaq.objects.create(product=product, email=request.user.email ,user=request.user, question=request.GET['question'])
    faq.save()
    return JsonResponse({'bool': True})
    
        

def add_to_cart(request):
    cart_product = {}
    

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'product_meta_title': request.GET['product_meta_title'],
        'product_is_digital': request.GET['product_is_digital'],
        'product_types_choices': request.GET['product_types_choices'],
        'shipping_amount': request.GET['shipping_amount'],
        'shipping_amount': request.GET['shipping_amount'],
        'vendor': request.GET['vendor'],
        'product_gz_coins': request.GET['product_gz_coins'],
        'product_brand': request.GET['product_brand'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        'product_processing_fee': request.GET['product_processing_fee'],
        'product_tax_fee': request.GET['product_tax_fee'],
        "product_stock_qty":request.GET["product_stock_qty"],
        "product_in_stock":request.GET["product_in_stock"],        

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:

            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

@csrf_exempt
def cart_view(request):
    
    cart_total_amount = 0
    total_shipping_amount = 0
    total_tax = 0
    total_amount = 0
    
    cart_total_amount_ = 0
    shipping_amount_ = 0
    total_amount_ = 0
    tax_amount = 0
    
    cart_total_amount_items = 0
    products_amount = 0
    service_fee_amount = 0
    service_fee_calc = 0
    tax_amount_ = 0
    shipping_amount__ = 0
    total_amount__ = 0
    processing_fee = 0
    processing_fee_ = 0
    order = []
    
    product_plus_shipping = 0
    
    main_cart_total = 0
    main_cart_total_item = 0
    # tax_rate = 0
    
    try:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
        # print("tax_rate =====================", tax_rate)
        # print("location_country =====================", location_country)
        
    except:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
        # print("location_country =====================", location_country)
        
    try:
        basic_addon = BasicAddon.objects.all().first()
        tax = basic_addon.general_tax_percentage / 100
        service_fee = basic_addon.service_fee_percentage / 100 
        service_fee_flat_rate = basic_addon.service_fee_flat_rate  
        vendor_fee = basic_addon.vendor_fee_percentage / 100 
    except:
        basic_addon = None
        tax = 0.5
        service_fee = 0.5
        vendor_fee = 0.5
        service_fee_flat_rate = 1
    
    if 'coupon_name' in request.session:
        vendor_coupon = Coupon.objects.filter(code=request.session['coupon_name'])
        print("vendor_coupon ===============", vendor_coupon)
    else:
        coupon_name = None
        

    if 'cart_data_obj' in request.session:
        
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total_shipping_amount += 0 #int(item['qty']) * float(item['shipping_amount'])
            total_tax += int(item['qty']) * float(tax_rate)
            products_amount += int(item['qty']) * float(item['price'])
            shipping_amount__ += 0 #int(item['qty']) * float(item['shipping_amount'])
            product_plus_shipping = products_amount + shipping_amount__
            
            # print("product_plus_shipping ==================", product_plus_shipping)
            # print("product_plus_shipping ==================", product_plus_shipping)
            # print("tax_amount_ ==================", tax_amount_)
            # print("tax_rate ==================", tax_rate)
            
            
            service_fee_calc = products_amount
            if basic_addon.service_fee_charge_type == "percentage":
                service_fee_amount = service_fee_calc * service_fee
                
            elif basic_addon.service_fee_charge_type == "flat_rate":
                service_fee_amount = service_fee_calc * float(service_fee_flat_rate)
                
            else:
                service_fee_amount = service_fee_calc * 0.5
                
                
            vendor = item['vendor']

            # total_amount = cart_total_amount + total_shipping_amount + total_tax + service_fee_amount
            main_cart_total = cart_total_amount + shipping_amount__
            tax_amount_ = main_cart_total * tax_rate
            
            total_amount = cart_total_amount + total_shipping_amount + service_fee_amount + tax_amount_
            
            product = Product.objects.get(id=p_id)
            
        # form = CheckoutForm()
        # if request.method == 'POST':
        #     form = CheckoutForm(request.POST)
        #     if form.is_valid():
        #         new_form = form.save(commit=False)
                
        #         full_name = new_form.full_name
        #         email = new_form.email
        #         mobile = new_form.mobile
        #         country = new_form.country
        #         state = new_form.state
        #         town_city = new_form.town_city
        #         address = new_form.address
                
                
        #         # tax_rate_fee = TaxRate.objects.filter(country=country)
        #         # if tax_rate_fee.exists():
        #         #     main_tax_fee = main_cart_total * tax_rate_fee.first().rate / 100
        #         #     print("tax_rate_fee ========================", main_tax_fee)
        #         # else:
        #         #     print("Failed ========================", tax_rate_fee)
        #         #     main_tax_fee = main_cart_total * 0.01
            
            
        #     main_tax_fee = main_cart_total * tax_rate
        #     total_amount__ = cart_total_amount + shipping_amount__ + main_tax_fee + service_fee_amount
        #     # print("main_tax_fee ==================", main_tax_fee)
            

        #     if request.user.is_authenticated:
        #         order = CartOrder.objects.create(
        #             full_name=full_name,
        #             email=email,
        #             mobile=mobile,
        #             country=country,
        #             state=state,
        #             town_city=town_city,
        #             address=address,
                    
        #             price=cart_total_amount, 
        #             buyer=request.user, 
        #             total=total_amount__, 
        #             shipping=shipping_amount__, 
        #             vat=main_tax_fee, 
        #             service_fee=service_fee_amount 
        #         )
        #         order.save()
        #     else:
        #         order = CartOrder.objects.create(
        #             full_name=full_name,
        #             email=email,
        #             mobile=mobile,
        #             country=country,
        #             state=state,
        #             town_city=town_city,
        #             address=address,
                    
        #             price=cart_total_amount, 
        #             buyer=None, 
        #             total=total_amount__, 
        #             shipping=shipping_amount__, 
        #             vat=main_tax_fee, 
        #             service_fee=service_fee_amount 
        #         )
        #         order.save()
        
        #     for p_id, item in request.session['cart_data_obj'].items():
        #         product = Product.objects.get(id=p_id)
        #         cart_total_amount_ += int(item['qty']) * float(item['price'])
        #         shipping_amount_ += int(item['qty']) * product.shipping_amount
        #         tax_amount += int(item['qty']) * float(tax)
        #         cart_total_amount_items = int(item['qty']) * float(item['price'])
        #         # Remove vendor fee from vendors products amounts
        #         total_payable = cart_total_amount_items -  vendor_fee
        #         item_shipping = int(item['qty']) * product.shipping_amount
                
        #         item_cart_total = int(item['qty']) * float(item['price'])
        #         main_cart_total_item = item_cart_total + float(item_shipping)
                
                
        #         service_fee_calc = products_amount
        #         # print("service_fee_calc ==================", service_fee_calc)
        #         if basic_addon.service_fee_charge_type == "percentage":
        #             service_fee_amount = service_fee_calc * service_fee
                    
        #         elif basic_addon.service_fee_charge_type == "flat_rate":
        #             service_fee_amount = service_fee_calc * float(service_fee_flat_rate)
                    
        #         else:
        #             service_fee_amount = service_fee_calc * 0.5

                
        #         tax_rate_fee = TaxRate.objects.filter(country=country)
        #         if tax_rate_fee.exists():
        #             main_tax_fee_item = main_cart_total_item * tax_rate_fee.first().rate / 100
        #             # print("tax_rate_fee ========================", main_tax_fee)
        #         else:
        #             # print("Failed ========================", tax_rate_fee)
        #             main_tax_fee_item = main_cart_total_item * 0.01
                
        #         grand_total = float(item['qty']) * float(item['price']) + float(item_shipping) + float(main_tax_fee_item) + float(service_fee_amount)
                
        #         cart_order_products = CartOrderItem.objects.create(
        #             order=order,
        #             vendor=product.vendor,
        #             invoice_no="#" + str(order.oid), 
        #             product=item['title'],
        #             image=item['image'],
        #             qty=item['qty'],
        #             product_obj=product,
        #             price=item['price'],
        #             shipping=item_shipping,
        #             paid_vendor=False,
        #             grand_total=grand_total,
        #             vat=main_tax_fee_item, 
        #             service_fee=service_fee_amount ,
        #             total_payable=total_payable,
        #             total=float(item['qty']) * float(item['price'])
        #         )
        #         cart_order_products.save()
        #         order.vendor.add(item['vendor'])

        #     return redirect('store:checkout', order.oid)
        now = timezone.now()
        if request.method == "POST":
            try:
                code = request.POST.get('code')
                coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
                print("coupon ===================", coupon.code)
                request.session['coupon_id'] = coupon.id
                request.session['coupon_name'] = coupon.code
                messages.success(request, f"Coupon Found and activated")
                return redirect("store:cart-view")
            except:
                messages.error(request, f"Coupon Not Found")
                return redirect("store:cart-view")
        else:
            form = CouponApplyForm()
        
        # del request.session['coupon_id']
        if 'coupon_name' in request.session:
            coupon_name = request.session['coupon_name']
        else:
            coupon_name = None
            
        context = {
            "cart_data":request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount':cart_total_amount, 
            'tax_amount_':tax_amount_, 
            'total_shipping_amount':total_shipping_amount , 
            'total_tax':total_tax, 
            'total_amount':total_amount,
            'service_fee_amount':service_fee_amount,
            'form':form,
            'coupon_name':coupon_name,
        }

        return render(request, "store/cart.html", context)
    else:
        messages.warning(request, "Your cart is empty, add something to the cart to continue")
        return redirect("store:home")


@csrf_exempt
def shipping_address(request):
    
    cart_total_amount = 0
    total_shipping_amount = 0
    total_tax = 0
    total_amount = 0
    
    cart_total_amount_ = 0
    shipping_amount_ = 0
    total_amount_ = 0
    tax_amount = 0
    
    cart_total_amount_items = 0
    products_amount = 0
    service_fee_amount = 0
    service_fee_amount_ = 0
    service_fee_calc = 0
    service_fee_calc_ = 0
    tax_amount_ = 0
    shipping_amount__ = 0
    total_amount__ = 0
    processing_fee = 0
    processing_fee_ = 0
    order = []
    products_amount__ = 0
    product_plus_shipping = 0
    
    main_cart_total = 0
    main_cart_total_item = 0
    # tax_rate = 0
    
    try:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
        # print("tax_rate =====================", tax_rate)
        # print("location_country =====================", location_country)
        
    except:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
        # print("location_country =====================", location_country)
        
    try:
        basic_addon = BasicAddon.objects.all().first()
        tax = basic_addon.general_tax_percentage / 100
        service_fee = basic_addon.service_fee_percentage / 100 
        service_fee_flat_rate = basic_addon.service_fee_flat_rate  
        vendor_fee = basic_addon.vendor_fee_percentage / 100 
    except:
        basic_addon = None
        tax = 0.5
        service_fee = 0.5
        vendor_fee = 0.5
        service_fee_flat_rate = 1

    digital_cart = False

    if 'cart_data_obj' in request.session:
        
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total_shipping_amount += 0 #int(item['qty']) * float(item['shipping_amount'])
            total_tax += int(item['qty']) * float(tax_rate)
            products_amount += int(item['qty']) * float(item['price'])
            shipping_amount__ += 0 #int(item['qty']) * float(item['shipping_amount'])
            product_plus_shipping = products_amount + shipping_amount__

            if item['product_is_digital'] == "True":
                digital_cart = True
                
            
            # print("product_plus_shipping ==================", product_plus_shipping)
            # print("product_plus_shipping ==================", product_plus_shipping)
            # print("tax_amount_ ==================", tax_amount_)
            # print("tax_rate ==================", tax_rate)
            
            service_fee_calc = products_amount
            if basic_addon.service_fee_charge_type == "percentage":
                service_fee_amount = service_fee_calc * service_fee
                
            elif basic_addon.service_fee_charge_type == "flat_rate":
                service_fee_amount = service_fee_calc * float(service_fee_flat_rate)
                
            else:
                service_fee_amount = service_fee_calc * 0.5
                
                

            # total_amount = cart_total_amount + total_shipping_amount + total_tax + service_fee_amount
            #main_cart_total = cart_total_amount + shipping_amount__
            tax_amount_ = main_cart_total * tax_rate
            
            total_amount = cart_total_amount + total_shipping_amount + service_fee_amount + tax_amount_
            
            product = Product.objects.get(id=p_id)
            
        if request.user.is_authenticated:
            form = CheckoutForm(user=request.user)
        else:
            form = CheckoutForm()
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            print(request.POST)
            if form.is_valid():
                print("payment_method", request.POST.get("payment_method"))
                new_form = form.save(commit=False)
                
                full_name = new_form.full_name
                email = new_form.email
                mobile = new_form.mobile
                country = new_form.country
                state = new_form.state
                town_city = new_form.town_city
                address = new_form.address
                shipping_method = request.POST.get("shipping_method")
                payment_method = request.POST.get("payment_method")
                billing_country = new_form.billing_country
                billing_state = new_form.billing_state
                billing_town_city = new_form.billing_town_city
                billing_address = new_form.billing_address
                
                print(digital_cart)
                if shipping_method == "ship_to_home" and digital_cart == False:
                    print("test")
                    # Add $7 to the total amount for shipping to home
                    shipping_amount__ = 7
                    total_shipping_amount = shipping_amount__
                    total_amount__ += total_shipping_amount


                # tax_rate_fee = TaxRate.objects.filter(country=country)
                # if tax_rate_fee.exists():
                #     main_tax_fee = main_cart_total * tax_rate_fee.first().rate / 100
                #     print("tax_rate_fee ========================", main_tax_fee)
                # else:
                #     print("Failed ========================", tax_rate_fee)
                #     main_tax_fee = main_cart_total * 0.01
            
            
            main_tax_fee = main_cart_total * tax_rate
            total_amount__ = cart_total_amount + total_shipping_amount + main_tax_fee + service_fee_amount
            # print("main_tax_fee ==================", main_tax_fee)
            

            if request.user.is_authenticated:
                order = CartOrder.objects.create(
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                    country=country,
                    state=state,
                    town_city=town_city,
                    address=address,
                    shipping_method=shipping_method,
                    payment_method=payment_method,

                    billing_country=billing_country,
                    billing_state=billing_state,
                    billing_town_city=billing_town_city,
                    billing_address=billing_address,
                    
                    price=cart_total_amount, 
                    buyer=request.user, 
                    total=total_amount__, 
                    original_total=total_amount__,
                    shipping=shipping_amount__, 
                    vat=main_tax_fee, 
                    service_fee=service_fee_amount 
                )
                order.save()
            else:
                if request.user.is_authenticated:
                    userr = request.user
                else:
                    userr = None
                order = CartOrder.objects.create(
                    full_name=full_name,
                    email=email,
                    mobile=mobile,
                    country=country,
                    state=state,
                    town_city=town_city,
                    address=address,
                    shipping_method=shipping_method,  # Include shipping_method here
                    payment_method=payment_method,  # Include payment_method here

                    billing_country=billing_country,
                    billing_state=billing_state,
                    billing_town_city=billing_town_city,
                    billing_address=billing_address,

                    price=cart_total_amount, 
                    buyer=userr, 
                    total=total_amount__, 
                    original_total=total_amount__,
                    shipping=shipping_amount__, 
                    vat=main_tax_fee, 
                    service_fee=service_fee_amount 
                )
                order.save()
        
            for p_id, item in request.session['cart_data_obj'].items():
                product = Product.objects.get(id=p_id)

                cart_total_amount_ += int(item['qty']) * float(item['price'])
                shipping_amount_ += int(item['qty']) * product.shipping_amount
                tax_amount += float(item['qty']) * tax_rate
                cart_total_amount_items = int(item['qty']) * float(item['price'])
                # Remove vendor fee from vendors products amounts
                total_payable = cart_total_amount_items -  vendor_fee
                item_shipping = int(item['qty']) * product.shipping_amount
                
                item_cart_total = int(item['qty']) * float(item['price'])
                main_cart_total_item = item_cart_total + float(item_shipping)
                
                products_amount__ = int(item['qty']) * float(item['price'])
                
                service_fee_calc_ = products_amount__
                # print("service_fee_calc ==================", service_fee_calc)
                if basic_addon.service_fee_charge_type == "percentage":
                    service_fee_amount_ = service_fee_calc_ * service_fee
                    
                elif basic_addon.service_fee_charge_type == "flat_rate":
                    service_fee_amount_ = service_fee_calc_ * float(service_fee_flat_rate)
                    
                else:
                    service_fee_amount_ = service_fee_calc_ * 0.5

                
               
                main_tax_fee_item = main_cart_total_item * tax_rate
                print("main_tax_fee_item ========================", main_tax_fee_item)
                print("service_fee_amount ========================", service_fee_amount_)
                
                
                grand_total = float(item['qty']) * float(item['price']) + float(item_shipping) + float(main_tax_fee_item) + float(service_fee_amount_)
                original_grand_total = float(item['qty']) * float(item['price']) + float(item_shipping) + float(main_tax_fee_item) + float(service_fee_amount_)
                cart_order_products = CartOrderItem.objects.create(
                    order=order,
                    vendor=product.vendor,
                    invoice_no="#" + str(order.oid), 
                    product=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    product_obj=product,
                    price=item['price'],
                    shipping=item_shipping,
                    gz_coins=item['product_gz_coins'],
                    product_types_choices=item['product_types_choices'],
                    paid_vendor=False,
                    original_grand_total=original_grand_total,
                    grand_total=grand_total,
                    vat=main_tax_fee_item, 
                    service_fee=service_fee_amount_ ,
                    total_payable=total_payable,
                    total=float(item['qty']) * float(item['price'])
                )
                cart_order_products.save()
                order.vendor.add(item['vendor'])

            return redirect('store:checkout', order.oid)

        context = {
            "cart_data":request.session['cart_data_obj'], 
            'totalcartitems': len(request.session['cart_data_obj']), 
            'cart_total_amount':cart_total_amount, 
            'tax_amount_':tax_amount_, 
            'total_shipping_amount':total_shipping_amount , 
            'total_tax':total_tax, 
            'total_amount':total_amount,
            'service_fee_amount':service_fee_amount,
            'form':form
        }

        return render(request, "store/shipping_address.html", context)
    else:
        messages.warning(request, "Your cart is empty, add something to the cart to continue")
        return redirect("store:home")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    basic_addon = BasicAddon.objects.all().first()
    tax = basic_addon.general_tax_percentage / 100
    cs = basic_addon.currency_sign
    
    try:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
    except:
        tax_rate = None
        tax_country = "united States"

    cart_total_amount = 0
    shipping_amount_ = 0
    total_amount = 0
    tax_amount = 0
    product_processing_fee_ = 0
    total_plus_shipping = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            shipping_amount_ += int(item['qty']) * float(item['shipping_amount'])
            
            total_plus_shipping = cart_total_amount + shipping_amount_
            
            product_processing_fee_ = int(cart_total_amount) * float(item['product_processing_fee'])
            tax_amount = total_plus_shipping * tax_rate

            total_amount = cart_total_amount + shipping_amount_ + tax_amount + product_processing_fee_
            
            # Fetch the product object from the database
            product = get_object_or_404(Product, pid=item['pid'])
            # Add meta_title to the item dictionary
            item['meta_title'] = product.meta_title  # Assuming the meta_title attribute exists on the Product model

    context = render_to_string("store/async/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'total_shipping_amount': shipping_amount_, 'total_tax': tax_amount, "cs": cs, 'total_amount': total_amount, 'product_processing_fee_': product_processing_fee_, "tax_country": tax_country})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    shipping_amount = request.GET['shipping_amount']
    product_tax_fee = request.GET['product_tax_fee']
    product_processing_fee = request.GET['product_processing_fee']
    

    basic_addon = BasicAddon.objects.all().first()
    tax = basic_addon.general_tax_percentage / 100
    cs = basic_addon.currency_sign
    
    try:
        location_country = "Tunisia"
        tax_country = TaxRate.objects.filter(country=location_country).first()
        tax_rate = tax_country.rate / 100
    except:
        tax_rate = None

    # print("product_tax_fee =====================", product_tax_fee)


    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            cart_data[str(request.GET['id'])]['shipping_amount'] = 0
            cart_data[str(request.GET['id'])]['product_tax_fee'] = product_tax_fee
            cart_data[str(request.GET['id'])]['product_processing_fee'] = product_processing_fee
            request.session['cart_data_obj'] = cart_data
    
    cart_total_amount = 0
    shipping_amount_ = 0
    total_amount = 0
    tax_amount = 0
    product_processing_fee_ = 0
    total_plus_shipping = 0
    
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            shipping_amount_ += 0 #int(item['qty']) * float(item['shipping_amount'])
            
            total_plus_shipping = cart_total_amount + shipping_amount_
            
            product_processing_fee_ = int(cart_total_amount) * float(item['product_processing_fee'])
            tax_amount = total_plus_shipping * tax_rate

            total_amount = cart_total_amount + shipping_amount_ + tax_amount + product_processing_fee_
            
            # print("int(total_plus_shipping) =====================", int(total_plus_shipping))
            # print("float(item['product_tax_fee'] =====================", float(item['product_tax_fee']))
            
            

    context = render_to_string("store/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount ,  'total_shipping_amount':shipping_amount_ , 'total_tax':tax_amount, "cs":cs, 'total_amount':total_amount, 'product_processing_fee_':product_processing_fee_})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def checkout_view(request, oid, *args, **kwargs):
    try:
        order = CartOrder.objects.get(oid=oid)
        if order.payment_status == "paid":
            messages.warning(request, "This Order have been paid for.")
            return redirect("core:buyer-dashboard")
        
        address = CartOrder.objects.get(oid=oid)
        order_items = CartOrderItem.objects.filter(order=order)
        # print("order_email =============", order.email)
        order.payment_status = "processing"
        order.order_status = "initiated"
        # After the order is successfully created and saved
        order.save()

        # Iterate over each product in the order
        #for product_item in order.cartorderitem_set.all():
        #    # Access the user associated with the product
        #    product_user = product_item.product_obj.user
        #
        #    # Update gz_coins for the user by adding the gz_coins of the product
        #    #product_user.gz_coins += product_item.gz_coins
        #    #product_user.save()
                
        now = timezone.now()
        if request.method == "POST":
            try:
                if request.user.is_authenticated:
                    code = request.POST.get('code')
                    coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
                    type = coupon.type
                    print("type =============", type)

                    order_items_ = CartOrderItem.objects.filter(vendor=coupon.vendor, order=order)

                    for o in order_items_:
                        # if o.applied_coupon == False:
                        if not coupon in o.coupon.all():

                            
                            if type == "Percentage":

                                calc = o.total * coupon.discount / 100
                                o.coupon_discount_grand_total = o.grand_total - calc
                                coupon.redemption += 1
                                
                                # Order
                                order.coupons.add(coupon)
                                order.total -= calc
                                order.price -= calc
                                order.saved += calc
                                
                                # Order Items
                                o.coupon.add(coupon)
                                o.total_payable -= calc 
                                o.grand_total -= calc
                                o.saved += calc
                                o.applied_coupon = True
                                order.save()
                                o.save()
                                coupon.save()


                            elif type == "Flat Rate":

                                calc = coupon.discount

                                o.coupon_discount_grand_total = o.grand_total - calc
                                coupon.redemption += 1
                                
                                # Order
                                order.coupons.add(coupon)
                                order.total -= calc
                                order.price -= calc
                                order.saved += calc
                                
                                # Order Items
                                o.coupon.add(coupon)
                                o.total_payable -= calc 
                                o.grand_total -= calc
                                o.saved += calc
                                o.applied_coupon = True
                                order.save()
                                o.save()
                                coupon.save()
                                print("o.calc ==========", calc)
                                print("o.coupon_discount_grand_total ==========", o.coupon_discount_grand_total)
                            
                            else:
                                messages.error(request, f"Coupon Have No Discount Type")
                                return redirect("store:checkout", order.oid)

                        else:
                            messages.warning(request, f"Coupon Already Activated")
                            return redirect("store:checkout", order.oid)
                    messages.success(request, f"Coupon Found and activated")
                    return redirect("store:checkout", order.oid)
                else:
                    code = request.POST.get('code')
                    coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
                    
                    order_items_ = CartOrderItem.objects.filter(vendor=coupon.vendor, order=order)
                    for o in order_items_:
                        if not coupon in o.coupon.all():
                            
                            calc = o.grand_total * coupon.discount / 100
                            o.coupon_discount_grand_total = o.grand_total - calc
                            coupon.redemption += 1
                            
                            # Order
                            order.coupons.add(coupon)
                            order.total -= calc
                            order.price -= calc
                            order.saved += calc
                            
                            # Order Items
                            # o.coupon = coupon
                            o.coupon.add(coupon)
                            o.total_payable -= calc 
                            o.grand_total -= calc
                            o.saved += calc
                            o.applied_coupon = True
                            order.save()
                            o.save()
                            coupon.save()
                            print("o.calc ==========", calc)
                            print("o.coupon_discount_grand_total ==========", o.coupon_discount_grand_total)
                        else:
                            messages.warning(request, f"Coupon Already Activated")
                            return redirect("store:checkout", order.oid)
                    messages.success(request, f"Coupon Found and activated")
                    return redirect("store:checkout", order.oid)

            except Coupon.DoesNotExist:
                messages.error(request, f"Coupon Not Found")
                return redirect("store:checkout", order.oid)
        else:
            form = CouponApplyForm()
        
        if 'coupon_id' in request.session:
            del request.session['coupon_id']
            del request.session['coupon_name']
    
        
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': order.total,
            'item_name': "Order-Item-No-" + str(order.id),
            'invoice': "INVOICE_NO-" + str(timezone.now()),
            'currency_code': "USD",
        }
        
        paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    except CartOrder.DoesNotExist:
        messages.warning(request, "The order you are trying is access does not exist.")
        return redirect("store:home")
    context = {
        "order":order, 
        "address":address, 
        "order_items":order_items, 
        "paypal_payment_button":paypal_payment_button, 
        "stripe_publishable_key":settings.STRIPE_PUBLISHABLE_KEY, 
        }

    return render(request, "store/checkout.html", context)



def custom_checkout_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    address = CartOrder.objects.get(oid=oid)
    order_items = CartOrderItem.objects.filter(order=order)
    print("order_email =============", order.email)

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.total,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice': "INVOICE_NO-" + str(timezone.now()),
        'currency_code': "USD",
        'notify_url': 'http://{}{}'.format(host, reverse("store:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("store:payment-completed", kwargs={'oid': order.oid})),
        'cancel_url': 'http://{}{}'.format(host, reverse("store:payment-failed")),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    context = {
        "paypal_payment_button":paypal_payment_button, 
        "order":order, 
        "address":address, 
        "order_items":order_items, 
        "stripe_publishable_key":settings.STRIPE_PUBLISHABLE_KEY, 
    }

    return render(request, "store/checkout2.html", context)

class PaymentConfirmation(DetailView):
    model = CartOrder
    template_name = "payment/payment_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(PaymentConfirmation, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context  
    
from django.core.mail import send_mail

def PaymentSuccessView(request):
    payment_ref = request.GET.get('payment_ref')
    if payment_ref is None:
        return HttpResponseNotFound()
    
    # Fetch the order associated with the payment reference
    order = get_object_or_404(CartOrder, payment_ref=payment_ref)
    
    
    
    if order.payment_status == "processing":
        order.payment_status = "paid"
        order.payment_method = "Credit/Debit Card"
        order.delivery_status = "shipping_processing"
        order.save()
        
        request.session.pop('cart_data_obj')
        # Update order items, send email notifications, update product stock, and payout vendors
        update_order_details(order)
        
    elif order.payment_status == "paid":
        request.session.pop('cart_data_obj')
        messages.success(request, f'Your order has been received.')
        return redirect("core:buyer-order-detail", oid=order.oid)
    else:
        messages.success(request, 'Oops... Internal Server Error; please try again later')
        return redirect("store:home")
        
    products = CartOrderItem.objects.filter(order=order)
    return render(request, "payment/payment_success.html", {"order": order, 'products': products}) 

def update_order_details(order):
    # Update order items
    CartOrderItem.objects.filter(order=order, order__payment_status="processing").update(paid=True, delivery_status="shipping_processing")
    
    order_items = CartOrderItem.objects.filter(order=order, order__payment_status="processing")
    
    company = Company.objects.all().first()
    basic_addon = BasicAddon.objects.all().first()

    # Send email notifications to the customer
    if basic_addon.send_email_notifications:
        merge_data = {
            'company': company, 
            'order': order, 
            'order_items': order_items, 
        }
        subject = f"Order Placed Successfully. ID {order.oid}"
        text_body = render_to_string("email/message_body.txt", merge_data)
        html_body = render_to_string("email/message_customer.html", merge_data)
        
        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.FROM_EMAIL,
            to=[order.email], body=text_body
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()

    # Update product stock and perform vendor payouts
    for order_item in order_items:
        order_item.product_obj.stock_qty -= order_item.qty
        order_item.product_obj.save()
        
        amount = order_item.total_payable + order_item.shipping
        
        PayoutTracker.objects.create(vendor=order_item.vendor, currency=order_item.vendor.currency, amount=amount, item=order)
        Notification.objects.create(vendor=order_item.vendor, user=order_item.vendor.user, type="new_order", product=order_item.product_obj, amount=amount, order=order)
        
        if basic_addon.send_email_notifications:
            # Vendor Email
            merge_data = {
                'company': company, 
                'o': order_item, 
            }
            subject = f"New Order for {order_item.product_obj.title}"
            text_body = render_to_string("email/message_body.txt", merge_data)
            html_body = render_to_string("email/message_body.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject, from_email=settings.FROM_EMAIL,
                to=[order_item.vendor.shop_email], body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()

"""     # Update vendor wallets
    for vendor in order.vendor.all():
        cart_order_items = CartOrderItem.objects.filter(order=order, order__payment_status="processing", vendor=vendor).aggregate(amount=models.Sum(F('total_payable') + F('shipping')))
        
        basic_addon = BasicAddon.objects.all().first()
        
        if basic_addon.payout_vendor_fee_immediately:
            if vendor.payout_method == 'payout_to_wallet':
                vendor.wallet += cart_order_items['amount']
                vendor.save()
        else:
            vendor.wallet += cart_order_items['amount']
            vendor.save() """

def PaymentFailedView(request):
    payment_ref = request.GET.get('payment_ref')
    if payment_ref is None:
        return HttpResponseNotFound()
    
    # Fetch the order associated with the payment reference
    order = get_object_or_404(CartOrder, payment_ref=payment_ref)
    
    # Update the order status for failed payment
    order.payment_status = "failed"
    order.save()
    
    return render(request, "payment/payment_failed.html", {"order": order}) 

@csrf_exempt
def create_checkout_session(request, id):
    print("Create checkout session")
    order = get_object_or_404(CartOrder, oid=id)
    order.order_status = "pending"
    order.save()
    if order.payment_method == "credit_card":
        request_data = json.loads(request.body)
    try:
        request.session.pop('cart_data_obj')
    except:
        pass
    print(order.payment_method)

    for product_item in order.cartorderitem_set.all():
        print(product_item)
        # Access the user associated with the product
        product_user = product_item.product_obj.user
        # Update gz_coins for the user by adding the gz_coins of the product
        if product_user:
            product_user.gz_coins += product_item.gz_coins
            product_user.save()
    if order.payment_method == "cash":
        messages.success(request, f'Your order has been received.')
        return redirect('store:payment-completed', oid=order.oid)


    # Call initiate_payment to start the payment process
    payment_data = initiate_payment(request, orderId=id, amount=order.total)
    
    try:
        response_json = payment_data.json()
        if "paymentRef" in response_json:
            payment_ref = response_json["paymentRef"]
            # Construct success and fail URLs
            success_url = request.build_absolute_uri(reverse('store:success'))
            fail_url = request.build_absolute_uri(reverse('store:failed'))

            # Update order with payment reference
            order.payment_status = "processing"
            order.payment_ref = payment_ref  # Save payment_ref to the order
            order.save()

            # Return the payment URL and payment reference to frontend
            return JsonResponse({"payUrl": response_json["payUrl"], "paymentRef": payment_ref})
        else:
            # If payment initiation fails, return error response
            return JsonResponse({"error": response_json.get("error", "Unknown error")}, status=400)
    except json.JSONDecodeError:
        # If the response is not in JSON format
        return HttpResponseBadRequest("Invalid JSON response from payment gateway")

def initiate_payment(request, orderId, amount):
    # Replace these values with your actual credentials and data for the production environment
    api_key = '65ddd6aecb4e3b38d7769896:wHwnU5eqcpICZvBCLIpoVnBonfJ'
    konnect_wallet_id = '65ddd6aecb4e3b38d776989a'

    # Update the URL to point to the production API endpoint
    url = "https://api.konnect.network/api/v2/payments/init-payment"

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    webhook_url = request.build_absolute_uri(reverse('store:webhook'))
    success_url = request.build_absolute_uri(reverse('store:success'))
    fail_url = request.build_absolute_uri(reverse('store:failed'))
    amount_float = float(amount)
    if request.user.is_authenticated:
        profile = request.user.profile

        payload = {
            "receiverWalletId": konnect_wallet_id,
            "token": "TND",
            "amount": amount_float * 1000,  # Convert to smallest currency unit
            "type": "immediate",
            "description": "payment description",
            "acceptedPaymentMethods": ["bank_card"],
            "lifespan": 10,
            "checkoutForm": True,
            "addPaymentFeesToAmount": True,
            "firstName": profile.user.first_name,  # Access user's first name from profile
            "lastName": profile.user.last_name,    # Access user's last name from profile
            "phoneNumber": profile.phone,          # Access phone from profile
            "email": profile.user.email,           # Access user's email from profile
            "orderId": orderId,
            "webhook": webhook_url,
            "silentWebhook": True,
            "successUrl": success_url,
            "failUrl": fail_url,
            "theme": "dark"
        }
    else:
        order = CartOrder.objects.get(oid=orderId)

        payload = {
            "receiverWalletId": konnect_wallet_id,
            "token": "TND",
            "amount": amount_float * 1000,  # Convert to smallest currency unit
            "type": "immediate",
            "description": "payment description",
            "acceptedPaymentMethods": ["bank_card"],
            "lifespan": 10,
            "checkoutForm": True,
            "addPaymentFeesToAmount": True,
            "firstName": order.full_name,
            "lastName": order.full_name, 
            "phoneNumber": order.mobile, 
            "email": order.email,        
            "orderId": orderId,
            "webhook": webhook_url,
            "silentWebhook": True,
            "successUrl": success_url,
            "failUrl": fail_url,
            "theme": "dark"
        }

    response = requests.post(url, headers=headers, json=payload, verify=False)
    print(response.content)
    if response.status_code == 200:
        data = response
        return data
    else:
        error_message = "Failed to initiate payment"
        return {"error": error_message}

def webhook(request):
    payment_ref = request.GET.get("payment_ref")
    if payment_ref:
        # Query Konnect API to get payment details
        payment_status = get_payment_status(payment_ref)
        print(payment_status)
        # Process payment status and update database or trigger actions
        # Example: Update database with payment status
        # payment.update(status=payment_status)
        return JsonResponse({"message": "Webhook received", "payment status": payment_status})
    else:
        return JsonResponse({"error": "Payment reference ID not provided"})

def get_payment_status(payment_ref):
    # Make a request to Konnect API to get payment details
    # Replace 'YOUR_KONNECT_API_KEY' with your actual API key
    api_key = '665ddd89ecb4e3b38d776b78a:5usETKkdz0MZwYpgWLMIQXg2gtyNgGp'
    url = f"https://api.preprod.konnect.network/api/v2/payments/{payment_ref}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_data = response.json()
        payment_status = payment_data.get("payment", {}).get("status")
        return payment_status
    else:
        error_message = "Failed to get payment status"
        if response.status_code == 401:
            error_message = "Unauthorized: API key is invalid or missing"
        elif response.status_code == 403:
            error_message = "Forbidden: You do not have permission to access this resource"
        elif response.status_code == 404:
            error_message = "Not Found: The requested resource was not found"
        elif response.status_code == 422:
            error_message = "Unprocessable Entity: The request was well-formed but failed validation"
        elif response.status_code == 502:
            error_message = "Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server"
        
        return error_message


def payment_completed_view(request, oid, *args, **kwargs):
    order = CartOrder.objects.get(oid=oid)
    if order.payment_method == "cash":
        order.payment_status = "pending"
        order.delivery_status = "shipping_processing"
        order.save()

    if order.payment_status == "pending" and order.payment_method == "credit_card":
        order.payment_status = "paid"
        order.delivery_status = "shipping_processing"
        order.save()
        
        
        CartOrderItem.objects.filter(order=order, order__payment_status="paid").update(paid=True, delivery_status="shipping_processing")
        order_items = CartOrderItem.objects.filter(order=order, order__payment_status="paid")
        
        
        company = Company.objects.all().first()
        basic_addon = BasicAddon.objects.all().first()
        if basic_addon.send_email_notifications == True:
            merge_data = {
                'company': company, 
                'order': order, 
                'order_items': order_items, 
            }
            subject = f"Order Placed Successfully. ID {order.oid}"
            text_body = render_to_string("email/message_body.txt", merge_data)
            html_body = render_to_string("email/message_customer.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject, from_email=settings.FROM_EMAIL,
                to=[order.email], body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()

        
        for o in order_items:
            o.product_obj.stock_qty -= o.qty
            o.product_obj.save()
            
            amount = o.total_payable +  o.shipping
            
            PayoutTracker.objects.create(vendor=o.vendor, currency=o.vendor.currency, amount=amount, item=order)
            Notification.objects.create(vendor=o.vendor, user=o.vendor.user, type="new_order", product=o.product_obj, amount=amount, order=o.order)
            
            company = Company.objects.all().first()
            basic_addon = BasicAddon.objects.all().first()
            if basic_addon.send_email_notifications == True:
                merge_data = {
                    'company': company, 
                    'o': o, 
                }
                subject = render_to_string("email/message_subject.txt", merge_data).strip()
                text_body = render_to_string("email/message_body.txt", merge_data)
                html_body = render_to_string("email/message_body.html", merge_data)
                
                msg = EmailMultiAlternatives(
                    subject=subject, from_email=settings.FROM_EMAIL,
                    to=[o.vendor.shop_email], body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()
                
            
        for o in order.vendor.all():
        
            # cart_order_items = CartOrderItem.objects.filter(order=order, order__payment_status="paid", vendor=o).aggregate(amount=models.Sum('total_payable'))
            
            cart_order_items = CartOrderItem.objects.filter(order=order, order__payment_status="paid", vendor=o).aggregate(amount=models.Sum(F('total_payable') + F('shipping')))
            print("cart_order_items =========", round(cart_order_items['amount'], 2))
            basic_addon = BasicAddon.objects.all().first()
            
            if basic_addon.payout_vendor_fee_immediately == True:
                if o.payout_method == 'payout_to_stripe':
                    stripe.Transfer.create(
                        amount=int(cart_order_items['amount']) * 100,
                        currency="usd",
                        destination=o.stripe_user_id,
                        transfer_group="ORDER_95",
                    )
                    
                if o.payout_method == 'payout_to_paypal':
                    timestamp = d.now()
                    # timestamp = timezone.now()
                    username = settings.PAYPAL_CLIENT_ID
                    password = settings.PAYPAL_SECRET_ID
                    headers = {'Content-Type': 'application/json',}
                    data = '{"sender_batch_header": {"sender_batch_id": "Payouts_' + str(timestamp) + '","email_subject": "You have a payout!","email_message": "You have received a payout for an order!"},"items": [{"recipient_type": "EMAIL","amount": {"value": "'+ str(round(cart_order_items['amount'], 2)) +'","currency": "'+ str(o.currency) +'"},"note": "Thanks for your patronage!","sender_item_id": "201403140001","receiver": "'+ str(o.paypal_email_address) +'","notification_language": "en-US"}]}'
                    response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payouts', headers=headers, data=data, auth=(username, password))
                    
                    print("Response ============", response)
                    print("date ============", data)
                    
                if o.payout_method == 'payout_to_wallet':
                    o.wallet += cart_order_items['amount']
                    o.save()
            else:
                o.wallet += cart_order_items['amount']
                o.save()
            
            o.save()
        
    elif order.payment_status == "paid" or order.payment_method == "cash":
        messages.success(request, f'Your Order have been recieved.')
        return redirect("core:buyer-order-detail", oid=order.oid)
            
    elif order.payment_status == "pending":
        messages.success(request, f'Your Order have been recieved.')
        return redirect("core:buyer-order-detail", oid=order.oid)
    else:
        messages.success(request, 'Opps... Internal Server Error; please try again later')
        return redirect("store:home")
        
    products = CartOrderItem.objects.filter(order=order)
    
    context = {
        "order":order,
        'products':products,
    }
    return render(request, "payment/paypal_payment_success.html", context) 



def payment_failed_view(request):
    return render(request, "payment/paypal_payment_failed.html") 


def country_get(request):
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    
    # device_type = ""
    # browser_type = ""
    # browser_version = ""
    # os_type = ""
    # os_version = ""
    # if request.user_agent.is_mobile:
    #     device_type = "Mobile"
    # if request.user_agent.is_tablet:
    #     device_type = "Tablet"
    # if request.user_agent.is_pc:
    #     device_type = "PC"
    
    # browser_type = request.user_agent.browser.family
    # browser_version = request.user_agent.browser.version_string
    # os_type = request.user_agent.os.family
    # os_version = request.user_agent.os.version_string
    
    # g = GeoIP2()
    # location = g.city(ip)
    # location_country = location["country_name"]
    # location_city = location["city"]
    
    # tax = TaxRate.objects.filter(country=location_country, active=True).first()
    # print("NOTE: =================== ", tax)
    
    
        
    
    # context = {
    #     "ip": ip,
    #     "device_type": device_type,
    #     "browser_type": browser_type,
    #     "browser_version": browser_version,
    #     "os_type":os_type,
    #     "os_version":os_version,
    #     "location_country": location_country,
    #     "location_city": location_city
    # }
    return render(request, "store/country_get.html")


def pageNotFoundView(request, invalid_path=None):
    return render(request, '404.html', status=404)

def handler404(request, exception):
    return render(request, '404.html', status=404)