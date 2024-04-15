from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, F, FloatField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.db.models import OuterRef, Subquery
from django.core import serializers
from django.utils.text import slugify


from vendor.models import ChatMessage, Vendor, DeliveryCouriers, PayoutTracker, Notification, Coupon
from vendor.forms import VendorForm, ProductForm, GalleryDataFormSet, GalleryForm, DeliveryCouriersForm, CartOrderInvoiceForm, CartOrderItemsInvoiceForm, CartOrderItemDataFormSet, CartOrderForm, CartOrderItemForm,CartOrderItemFormset, FilteredCartOrderItemFormset, PayoutForm, CouponApplyForm

from addons.models import BasicAddon, Company, EarningPoints, NewsLetter, TaxRate
from userauths.models import Profile, User
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from store.models import CartOrder, CartOrderItem, Gallery, Product, Category, ProductOffers, ProductBidders, ProductFaq, Review
from store.forms import CartOrderItemForm
from reports.models import ProductReport, BiddingUserReport, OrderItemReport, VendoReport

from datetime import datetime, timedelta
import calendar
import urllib
import requests
import stripe
from datetime import datetime as d
from decimal import Decimal
from anymail.message import attach_inline_image_file
import shortuuid


one_week_ago = datetime.today() - timedelta(days=7)
one_month_ago = datetime.today() - timedelta(days=28)
ninety_days_ago = datetime.today() - timedelta(days=90)
five_days = datetime.now() - timedelta(days=5)


def check_user_vendor(request):
    if request.user.profile:
        messages.error(request, f"Hey {request.user.username}, you are not a vendor yet, create account now.")
        return redirect("vendor:become-vendor")

def become_a_vendor(request):
    if request.user.is_authenticated:
        if request.user.profile.seller == True:
            messages.error(request, f"Hey {request.user.username}, you are already a vendor.")
            return redirect("vendor:dashboard")
    return render(request, "vendor/become_vendor.html")

def vendor_registration(request):
    return render(request, "vendor/become_vendor.html")

def VendorRegister(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.user.profile.seller == True:
            messages.error(request, f"Hey {request.user.username}, you are already a vendor.")
            return redirect("vendor:dashboard")
        else:
            vendor = Vendor.objects.create(user=request.user, profile=request.user.profile, shop_email=request.user.email, shop_name=request.user.username)
            request.user.profile.seller = True 
            request.user.profile.save()
            messages.success(request, f"Your vendor account have been created successfully.")
            return redirect('vendor:settings')


    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_form = form.save()
        email = form.cleaned_data.get('username')
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        NewsLetter.objects.create(email=username)
        messages.success(request, f"Hi {request.user.username}, your vendor account was created successfully, setup your shop now.")
        try:
            vendor = Vendor.objects.create(user=new_form, profile=new_form.profile, password=password, shop_name=email)
            new_form.profile.seller = True 
            new_form.profile.save()
        except print(0):
            pass
        

        return redirect('vendor:settings')
    
    context = {'form':form}
    return render(request, 'vendor/register.html', context)

@login_required
def vendor_shop_creation(request):
    if request.user.profile.seller != True:
        messages.error(request, f"Hey {request.user.username}, you are not a vendor yet, create account now.")
        return redirect("vendor:become-vendor")
    
    vendor = Vendor.objects.get(user=request.user, profile=request.user.profile)
    if request.method == "POST":
        form = VendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user 
            new_form.profile = request.user.profile 
            new_form.save()
            
            profile = Profile.objects.get(user=request.user)
            profile.full_name = new_form.shop_name
            profile.image = new_form.shop_image
            profile.save()
            
            messages.success(request, "Your shop have been successfully updated.")
            return redirect("vendor:settings")
    else:
        form = VendorForm(instance=vendor)
    context = {
        "form":form,
        "vendor":vendor,
    }    
    return render(request, "vendor/shop-creation.html", context)


@login_required
def vendor_dashboard(request):
    order = CartOrder.objects.filter(payment_status="paid", vendor=request.user.vendor).order_by("-id")[:20]
    total_sales_revenue = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid").aggregate(amount=models.Sum('total'))
    total_payable_revenue = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid").aggregate(amount=models.Sum('total_payable'))
    weekly_earning = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid", date__gte=one_week_ago).aggregate(amount=models.Sum('total'))
    total_orders = CartOrder.objects.filter(vendor=request.user.vendor, payment_status="paid").order_by("-id")[:20]
    weekly_orders = CartOrder.objects.filter(vendor=request.user.vendor, payment_status="paid", date__gte=one_week_ago)
    customer = CartOrder.objects.filter(vendor=request.user.vendor, payment_status="paid")
    new_order = CartOrder.objects.filter(payment_status="paid", vendor=request.user.vendor, date__gte=five_days).order_by("-id")
    
    notification = Notification.objects.filter(vendor=request.user.vendor, seen=False).order_by("-id")[:10]
    total_payout = PayoutTracker.objects.filter(vendor=request.user.vendor).aggregate(amount=models.Sum('amount'))
        
    output = CartOrder.objects.filter(vendor=request.user.vendor, payment_status="paid").annotate(month=ExtractMonth("date")).values("month").annotate(count=Count("id"),).order_by("month")
    # earning = CartOrderItem.objects.filter(vendor=request.user.vendor, paid=True).annotate(month=ExtractMonth("date")).values("month").annotate(count=Sum("total_payable"),).order_by("month")
    
    monthNumber=[]
    totalOrders=[]
    
    earningMonthNumber=[]
    totalEarning=[]


    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
        
    # for d in earning:
    #     earningMonthNumber.append(calendar.month_name[d['month']])
    #     totalEarning.append(Round(d['count'], 2))
    
    context = {
        "total_payout":total_payout,
        "earningMonthNumber":earningMonthNumber,
        "totalEarning":totalEarning,
        "monthNumber":monthNumber,
        "totalOrders":totalOrders,
        "total_sales_revenue":total_sales_revenue,
        "total_payable_revenue":total_payable_revenue,
        "notification":notification,
        # "earning":earning,
        "new_order":new_order,
        "order":order,
        "weekly_earning":weekly_earning,
        "total_orders":total_orders,
        "weekly_orders":weekly_orders,
        "customer":customer,
    } 
    return render(request, "vendor/dashboard.html", context)



@login_required
def vendor_orders(request):
    five_days = datetime.now() - timedelta(days=5)
    
    order = CartOrder.objects.filter(payment_status="paid", vendor=request.user.vendor).order_by("-id")
    orders = CartOrder.objects.filter(payment_status="paid", vendor=request.user.vendor).order_by("-id")
    new_order = CartOrder.objects.filter(payment_status="paid", vendor=request.user.vendor, date__gte=five_days).order_by("-id")
    
    query = request.GET.get("q")
    if query:
        order = order.filter(Q(oid__icontains=query)).distinct()
    
    # Pagination Function
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    context = {
        "order":order,
        "five_days":five_days,
        "new_order":new_order,
    } 
    return render(request, "vendor/vendor-order.html", context)


@login_required
def order_delivery_status(request, status):
    products = Product.objects.filter(vendor=request.user.vendor, status=status)

    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(tags__name__icontains=query)|
            Q(category__title__icontains=query)
            ).distinct()
    
    # Pagination Function
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products":products,
    } 
    return render(request, "vendor/product-status.html", context)


@login_required
def vendor_order_detail(request, oid):
    order = CartOrder.objects.get(vendor=request.user.vendor, oid=oid)
    order_items = CartOrderItem.objects.filter(order=order, vendor=request.user.vendor)
    shipping = CartOrderItem.objects.filter(order=order, vendor=request.user.vendor).aggregate(amount=models.Sum('shipping'))
    total = CartOrderItem.objects.filter(order=order, vendor=request.user.vendor).aggregate(amount=models.Sum('total'))
    earning = CartOrderItem.objects.filter(order=order, vendor=request.user.vendor).aggregate(amount=models.Sum('total_payable'))
    
    context = {
        "order":order,
        "order_items":order_items,
        "shipping":shipping,
        "total":total,
        "earning":earning,

    } 
    return render(request, "vendor/order-detail.html", context)

@login_required
def vendor_products(request):
    products = Product.objects.filter(vendor=request.user.vendor).order_by("-id")
    products_count = Product.objects.filter(vendor=request.user.vendor).order_by("-id")
    
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(tags__name__icontains=query)|
            Q(category__title__icontains=query)
            ).distinct()
    
    # Pagination Function
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products":products,
        'products_count':products_count,
    } 
    return render(request, "vendor/products.html", context)


@login_required
def vendor_product_category(request, cid):
    category_product = Category.objects.get(cid=cid, active=True)
    products = Product.objects.filter(vendor=request.user.vendor, category=category_product)
    products_count = Product.objects.filter(vendor=request.user.vendor, category=category_product)
    
    
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(tags__name__icontains=query)|
            Q(category__title__icontains=query)
            ).distinct()
    
    # Pagination Function
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products":products,
        'category_product':category_product,
        'products_count':products_count,
    } 
    return render(request, "vendor/product-category.html", context)


@login_required
def vendor_product_status(request, status):
    products = Product.objects.filter(vendor=request.user.vendor, status=status)
    
    
    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(tags__name__icontains=query)|
            Q(category__title__icontains=query)
            ).distinct()
    
    # Pagination Function
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "products":products,
    } 
    return render(request, "vendor/product-status.html", context)


@login_required
def vendor_add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.vendor = request.user.vendor
            new_form.save()
            form.save_m2m()
            messages.success(request, f"Your product have been created successfully, it's now in review. We will notify you when the product is Live.")
            return redirect("vendor:products")
    else:
        form = ProductForm()
    context = {
        'form':form
    } 
    return render(request, "vendor/product-create.html", context)

@login_required
def vendor_edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.vendor = request.user.vendor
            new_form.save()
            form.save_m2m()
            messages.success(request, f"Your product have been updated.")
            return redirect("vendor:products")
    else:
        form = ProductForm(instance=product)
    context = {
        'form':form,
        'product':product,
    } 
    return render(request, "vendor/product-edit.html", context)


class ProductInline():
    form_class = ProductForm
    model = Product
    template_name = "vendor/create-product.html"

    def form_valid(self,  form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.vendor = self.request.user.vendor
        self.object.save()
        self.object.slug = slugify(self.object.title) + "-" + str(uniqueid.lower())
        self.object.save()

        form.save_m2m()
        

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
            messages.success(self.request, "Your Product have Been Created.")
        return redirect('vendor:products')

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        variants = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()

        for variant in variants:
            variant.product = self.object
            variant.save()


class ProductCreate(LoginRequiredMixin, ProductInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': GalleryDataFormSet(prefix='variants'),
            }
        else:
            return {
                'variants': GalleryDataFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants')
            }
    
    def dispatch(self, request ,*args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.profile.seller == False:
                messages.warning(self.request, "You must be a vendor to create a product.")
                return redirect("vendor:products")
        else:
            messages.warning(self.request, "You need to login to create bets")
            return redirect("userauths:sign-in")

        return super(ProductCreate, self).dispatch(request, *args, **kwargs)
    
    
class ProductUpdate(LoginRequiredMixin, ProductInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        return {
            'variants': GalleryDataFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
        }

    def dispatch(self, request ,*args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.warning(self.request, "You are not allowed to edit this product.")
            return redirect("vendor:products")
            
        return super(ProductUpdate, self).dispatch(request, *args, **kwargs)


def delete_variant(request, pk):
    try:
        variant = Gallery.objects.get(id=pk)
    except Gallery.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('vendor:edit-product', pk=variant.product.pid)

    variant.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('vendor:edit-product', pk=variant.product.pid)

@login_required
def vendor_coupon(request):
    coupon = Coupon.objects.filter(vendor=request.user.vendor)
    form = CouponApplyForm()

    query = request.GET.get("q")
    if query:
        coupon = coupon.filter(Q(code__icontains=query)).distinct()
    
    context = {
        "coupon":coupon,
        "form":form,
        "query":query
    }
    return render(request, "vendor/vendor-coupon.html", context)


@login_required
def create_coupon(request):
    if request.method == "POST":
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.vendor = request.user.vendor
            new_form.save()
            messages.success(request, f"'{new_form.code}' Coupon Created Successfully.")
            return redirect("vendor:vendor-coupon")
    else:
        messages.success(request, "An Error Occured")
        return redirect("vendor:vendor-coupon")

def update_coupon(request, cid):
    coupon = Coupon.objects.get(cid=cid)
    if request.method == "POST":
        form = CouponApplyForm(request.POST, instance=coupon)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.vendor = request.user.vendor
            new_form.save()
            messages.success(request, f"'{new_form.code}' Coupon Updated Successfully.")
            return redirect("vendor:vendor-coupon")
    else:
        form = CouponApplyForm(instance=coupon)
    
    context = {
        "coupon":coupon,
        "form":form
    }
    return render(request, "vendor/update_coupon.html", context)
    

@login_required
def delete_coupon(request, cid):
    coupon = Coupon.objects.get(cid=cid)
    coupon.delete()
    messages.success(request, f"'{coupon.code}' Coupon Deleted Successfully.")
    return redirect("vendor:vendor-coupon")
    


def mark_as_shipped(request):
    id = request.GET['id']
    order_item = CartOrderItem.objects.get(id=id)
    order_item.delivery_status = "shipped"
    order_item.save()

    data = {
        "bool": True,
        "status": order_item.delivery_status
    }
    
    
    return JsonResponse({"data":data})


def mark_as_arrived(request):
    id = request.GET['id']
    order_item = CartOrderItem.objects.get(id=id)
    order_item.delivery_status = "arrived"
    order_item.save()

    data = {
        "bool": True,
        "status": order_item.delivery_status
    }
    return JsonResponse({"data":data})


def mark_as_delivered(request):
    id = request.GET['id']
    order_item = CartOrderItem.objects.get(id=id)
    order_item.delivery_status = "delivered"
    order_item.save()

    data = {
        "bool": True,
        "status": order_item.delivery_status
    }
    return JsonResponse({"data":data})


def mark_as_seen(request):
    id = request.GET['id']
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()

    data = {
        "bool": True,
        "status": "Notification Removed."
    }
    return JsonResponse({"data":data})





@login_required
def vendor_earning(request):
    one_week_ago = datetime.today() - timedelta(days=7)
    one_month_ago = datetime.today() - timedelta(days=28)
    total_sales = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid", paid=True).aggregate(amount=models.Sum('total'))
    shipping_fees = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid", paid=True).aggregate(amount=models.Sum('shipping'))
    total_payout = PayoutTracker.objects.filter(vendor=request.user.vendor).aggregate(amount=models.Sum('amount'))
    
    total_sales_revenue = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid").aggregate(amount=models.Sum('total'))
    monthly_earning = CartOrderItem.objects.filter(vendor=request.user.vendor, order__payment_status="paid", date__gte=one_month_ago).aggregate(amount=models.Sum('total'))
    
    output = (
       CartOrderItem.objects
        .filter(vendor=request.user.vendor, paid=True)
        .annotate(
            month=ExtractMonth("date")
        )
        .values("month")
        .annotate(
            count=Sum("qty"),
            total=Sum(
                F("qty") * F("price"),
                output_field=FloatField()
            )
        )
        .order_by("month")
    )
    monthNumber=[]
    totalOrders=[]
    amountTotal=[]
    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
        amountTotal.append(d['total'])
    
    context = {
        "shipping_fees":shipping_fees,
        "total_sales":total_sales,
        "total_payout":total_payout,
        "total_sales_revenue":total_sales_revenue,
        "monthly_earning":monthly_earning,
        "output":output,
        "monthNumber":monthNumber,
        "totalOrders":totalOrders,
        "amountTotal":amountTotal,
    } 
    return render(request, "vendor/earning.html", context)


class StripeAuthorizeView(View):
    
    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        url = 'https://connect.stripe.com/oauth/authorize'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': f'http://127.0.0.1:8000/vendor/oauth/callback'
        }
        url = f'{url}?{urllib.parse.urlencode(params)}'
        return redirect(url)
    
    
class StripeAuthorizeCallbackView(View):
    
    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)
            # add stripe info to the seller
            stripe_user_id = resp.json()['stripe_user_id']
            stripe_access_token = resp.json()['access_token']
            stripe_refresh_token = resp.json()['refresh_token']
            seller = Vendor.objects.get(user=self.request.user)
            seller.stripe_access_token = stripe_access_token
            seller.stripe_user_id = stripe_user_id
            seller.stripe_refresh_token = stripe_refresh_token
            seller.save()
        url = reverse('vendor:dashboard')
        response = redirect(url)
        messages.success(self.request, "You stripe account have been connected.")
        return response
    


class VendorPayoutView(View):
    
    def get(self, request):
        
        prev = d.now()
        now = timezone.now()
        print("now =====================", str(prev))
        o = Vendor.objects.get(user=request.user)
        username = settings.PAYPAL_CLIENT_ID
        password = settings.PAYPAL_SECRET_ID
        headers = {'Content-Type': 'application/json',}
        data = '{"sender_batch_header": {"sender_batch_id": "Payouts_' + str(prev) + '","email_subject": "You have a payout!","email_message": "You have received a payout for an order!"},"items": [{"recipient_type": "EMAIL","amount": {"value": "'+ str(o.wallet) +'","currency": "'+ str(o.currency) +'"},"note": "Thanks for your patronage!","sender_item_id": "201403140001","receiver": "'+ str(o.paypal_email_address) +'","notification_language": "en-US"}]}'
    
        response = requests.post('https://api-m.sandbox.paypal.com/v1/payments/payouts', headers=headers, data=data, auth=(username, password))
        url = reverse('vendor:settings')
        
        print("Response ============", response)
        print("date ============", data)
        response = redirect(url)
        messages.success(self.request, "Amount paid")
        return response
    
    
@login_required
def add_tracking_id(request, coid ,oid):
    cart_order = CartOrder.objects.get(oid=coid)
    order_item = CartOrderItem.objects.get(oid=oid, order=cart_order)
    
    # Add Tracking ID
    if request.method == "POST":
        tracking_form = CartOrderItemForm(request.POST, instance=order_item)
        if tracking_form.is_valid():
            tracking_form.save()
            messages.success(request, "Tracking ID Addedd Successfully")
            return redirect("vendor:order-detail", cart_order.oid)
    else:
        tracking_form = CartOrderItemForm(instance=order_item)
        
        
        
    # Add Courier Service ID
    if request.method == "POST":
        dc_form = DeliveryCouriersForm(request.POST)
        if dc_form.is_valid():
            dc_form.save()
            messages.success(request, "New Courier Service Added")
            return redirect("vendor:add-trackingID", cart_order.oid, order_item.oid)
    else:
        dc_form = DeliveryCouriersForm(instance=order_item)
        
    context = {
        "tracking_form":tracking_form,
        "dc_form":dc_form,
    }

    return render(request, 'vendor/add-tracking.html', context)


@login_required
def create_order_invoice(request):
    
    
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        
        form = CartOrderInvoiceForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.buyer = user
            new_form.payment_status = "pending"
            new_form.save()
            new_form.vendor.add(request.user.vendor)
            messages.success(request, "Order Created, Now Add Order Items.")
            return redirect("vendor:create-order-item-invoice", new_form.oid)
    else:
        form = CartOrderInvoiceForm()
    
    context = {
        'form':form
    }
    return render(request, 'vendor/cart-order-invoice.html', context)


@login_required
def create_order_item_invoice(request, oid):
    order = CartOrder.objects.get(oid=oid)    
    if request.method == "POST":
        form = CartOrderItemsInvoiceForm(request.user,request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.order = order
            new_form.vendor = request.user.vendor
            new_form.save()
            # messages.success(request, "Order Created, Now Add Order Items.")
            return redirect("vendor:dashboard")
    else:
        form = CartOrderItemsInvoiceForm(request.user)
    
    context = {
        'form':form
    }
    return render(request, 'vendor/cart-order-item-invoice.html', context)



class CartOrderInline():
    form_class = CartOrderInvoiceForm
    model = CartOrder
    template_name = "vendor/cart-order-invoice.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response( self.get_context_data(form=form))
        
        user_id = self.request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        

        self.object = form.save(commit=False)
        self.object.buyer = user
        self.object.payment_status = "pending"
        self.object.save()
        

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
            messages.success(self.request, "Custom order have been created.")
        return redirect('vendor:products')

    def formset_variants_valid(self, formset):
        basic_addon = BasicAddon.objects.all().first()
        service_fee = basic_addon.service_fee_percentage / 100 
        service_fee_flat_rate = basic_addon.service_fee_flat_rate  
        
        variants = formset.save(commit=False) 
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
            
        

        for variant in variants:
            variant.order = self.object
            variant.vendor = self.request.user.vendor
            variant.invoice_no = self.object.oid
            variant.total = variant.qty * variant.price
            if basic_addon.service_fee_charge_type == "percentage":
                variant.total_payable = float(variant.total) - service_fee
                
            elif basic_addon.service_fee_charge_type == "flat_rate":
                variant.total_payable = float(variant.total) - service_fee_flat_rate
                
            else:
                variant.total_payable = variant.total - 2
            
            # variant.grand_total = variant.total + variant.shipping +

            variant.save()


class CartOrderCreate(LoginRequiredMixin, CartOrderInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super(CartOrderCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': CartOrderItemDataFormSet(prefix='variants'),
            }
        else:
            return {
                'variants': CartOrderItemDataFormSet( self.request.POST or None, self.request.user, self.request.FILES or None, prefix='variants')
            }
    
    def dispatch(self, request ,*args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.profile.seller == False:
                messages.warning(self.request, "You must be a vendor to create a product.")
                return redirect("vendor:products")
        else:
            messages.warning(self.request, "You need to login to create bets")
            return redirect("userauths:sign-in")

        return super(CartOrderCreate, self).dispatch(request, *args, **kwargs)
    
    
class CartOrderUpdate(LoginRequiredMixin, CartOrderInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(CartOrderUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    
    def get_named_formsets(self):
        return {
            'variants': CartOrderItemDataFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
        }

    def dispatch(self, request ,*args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.warning(self.request, "You are not allowed to edit this product.")
            return redirect("vendor:products")
            
        return super(CartOrderUpdate, self).dispatch(request, *args, **kwargs)



@login_required
def create_custom_order_with_items(request):
    template_name = 'vendor/create_custom_order_with_items.html'
    tax_rate = TaxRate.objects.filter(active=True)
    
    basic_addon = BasicAddon.objects.all().first()
    service_fee = basic_addon.service_fee_percentage / 100 
    service_fee_flat_rate = basic_addon.service_fee_flat_rate  
    
    if request.method == 'GET':
        cartorderform = CartOrderForm(request.GET or None)
        formset = FilteredCartOrderItemFormset(request.user, queryset=CartOrderItem.objects.none())
    elif request.method == 'POST':
        try:
            cartorderform = CartOrderForm(request.POST)
            formset = FilteredCartOrderItemFormset(request.user, request.POST)
            user_id = request.POST.get("user_id")
            check_user = User.objects.filter(id=user_id)
            if check_user.exists():
                if user_id != None:
                    buyer = User.objects.get(id=user_id)
                else:
                    messages.error(request, "User ID cannot be blank!")
                    return redirect('vendor:create_custom_order_with_items')

                if cartorderform.is_valid() and formset.is_valid():
                    cartorder = cartorderform.save(commit=False)
                    cartorder.buyer = buyer
                    cartorder.custom_order = True
                    cartorder.save()
                    cartorder.vendor.add(request.user.vendor)
                    cartorder.save()
                    
                    
                    
                    
                    for form in formset:
                        # so that `book` instance can be attached.
                        cartorderitem = form.save(commit=False)
                        cartorderitem.order = cartorder
                        cartorderitem.vendor = request.user.vendor
                        
                        cartorderitem.invoice_no = cartorder.oid
                        cartorderitem.total = cartorderitem.qty * cartorderitem.price
                        if basic_addon.service_fee_charge_type == "percentage":
                            cartorderitem.total_payable = float(cartorderitem.total) - service_fee
                            
                        elif basic_addon.service_fee_charge_type == "flat_rate":
                            cartorderitem.total_payable = float(cartorderitem.total) - service_fee_flat_rate
                            
                        else:
                            cartorderitem.total_payable = cartorderitem.total - 2
                        
                        main_total = float(cartorderitem.total) + float(cartorderitem.shipping) 
                        tax_rate_fee = TaxRate.objects.filter(country=cartorder.country)
                        # print("tax_rate_fee ========================", tax_rate_fee)
                        if tax_rate_fee.exists():
                            print("tax_rate_fee ========================", tax_rate_fee)
                            cartorderitem.vat = main_total * tax_rate_fee.first().rate / 100
                        else:
                            print("Failed ========================", tax_rate_fee)
                            cartorderitem.vat = main_total * 0.01

                        
                        cartorderitem.service_fee = Decimal(cartorderitem.total) * Decimal(service_fee)
                        cartorderitem.grand_total = float(cartorderitem.shipping) + float(cartorderitem.service_fee) + float(cartorderitem.total) + float(cartorderitem.vat)
                        
                        cartorder.service_fee += float(cartorderitem.service_fee)
                        cartorder.price += float(cartorderitem.total)
                        cartorder.shipping += float(cartorderitem.shipping)
                        cartorder.vat += float(cartorderitem.vat)
                        cartorder.total += float(cartorderitem.grand_total)
                        
                        cartorderitem.save()
                        cartorder.save()
                        
                    messages.success(request, "Order have been created, copy and share order link.")
                    return redirect('store:checkout2', cartorder.oid)
            else:
                messages.error(request, "User with ID does not Exists, Get the correct ID from the customer.")
                return redirect('vendor:create_custom_order_with_items')
        except:
            messages.error(request, "You must select at least one product.")
            return redirect('vendor:create_custom_order_with_items')
    return render(request, template_name, {
        'cartorderform': cartorderform,
        'formset': formset,
    })
    
   
@login_required 
def list_custom_order(request):
    order = CartOrder.objects.filter(vendor=request.user.vendor, custom_order=True).order_by("-id")
    new_order = CartOrder.objects.filter(payment_status="paid", custom_order=True, vendor=request.user.vendor, date__gte=five_days).order_by("-id")
    
    context = {
        'order':order,
        'new_order':new_order,
    }
    return render(request, 'vendor/custom-orders.html', context)    


@login_required
def payable_invoice(request, oid):
    order = CartOrder.objects.get(vendor=request.user.vendor, custom_order=True, oid=oid)
    order_items = CartOrderItem.objects.filter(order=order, vendor=request.user.vendor)
    
    context = {
        'order':order,
        'order_items':order_items,
    }
    return render(request, 'vendor/payable-invoice.html', context)    


@login_required
def order_product_status(request, status):
    order = CartOrder.objects.filter(vendor=request.user.vendor, payment_status=status)
    
    query = request.GET.get("q")
    if query:
        order = order.filter(Q(oid__icontains=query)).distinct()
    
    paginator = Paginator(order, 10)
    page_number = request.GET.get('page')
    order = paginator.get_page(page_number)
    
    context = {"order":order}   
    return render(request, "vendor/order-status.html", context)


@login_required
def product_biddings(request):
    products = Product.objects.filter(vendor=request.user.vendor, type="auction").order_by("-id")
    product = Product.objects.filter(vendor=request.user.vendor, type="auction")
    
    query = request.GET.get("q")
    if query:
        product = product.filter(Q(bid__icontains=query)).distinct()
    
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    product = paginator.get_page(page_number)
    
    context = {
        "products":products,
        "product":product,
    }   
    
    return render(request, "vendor/product_biddings.html", context)


@login_required
def product_bidding_detail(request, pid):
    product = Product.objects.get(vendor=request.user.vendor, pid=pid)
    bidders = ProductBidders.objects.filter(product=product, product__vendor=request.user.vendor).order_by("-price")
    
    context = {
        "product":product,
        "bidders":bidders,
        }   
    return render(request, "vendor/product_bidding_detail.html", context)



@login_required
def product_offers(request):
    products = Product.objects.filter(vendor=request.user.vendor, type="offer").order_by("-id")
    product = Product.objects.filter(vendor=request.user.vendor, type="offer").order_by("-id")
    
    query = request.GET.get("q")
    if query:
        product = product.filter(Q(bid__icontains=query)).distinct()
    
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    product = paginator.get_page(page_number)
    
    context = {
        "products":products,
        "product":product,
               }   
    return render(request, "vendor/product_offers.html", context)


@login_required
def product_offer_detail(request, pid):
    product = Product.objects.get(vendor=request.user.vendor, pid=pid)
    offers = ProductOffers.objects.filter(product=product, product__vendor=request.user.vendor).order_by("-id")
    
    context = {
        "product":product,
        "offers":offers,
        }   
    return render(request, "vendor/product_offer_detail.html", context)


def mark_as_accepted(request):
    id = request.GET['id']
    offer = ProductOffers.objects.get(id=id)
    offer.status = "accepted"
    offer.save()
    
    
    # Email ======================
    basic_addon = BasicAddon.objects.all().first()
    if basic_addon.send_email_notifications == True:
    
        company = Company.objects.all().first()
        merge_data = {
            'company': company, 
            'offer': offer, 
        }
        subject = f"Offer Accepted for {offer.product.title}"
        text_body = render_to_string("email/message_body.txt", merge_data)
        html_body = render_to_string("email/offer_accepted.html", merge_data)
        
        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.FROM_EMAIL,
            to=[offer.email], body=text_body
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
    # Email ==========================
    
    data = {
        "bool": True,
        "status": "Accepted"
    }
    return JsonResponse({"data":data})


def mark_as_rejected(request):
    id = request.GET['id']
    offer = ProductOffers.objects.get(id=id)
    offer.status = "rejected"
    offer.save()
    data = {
        "bool": True,
        "status": "Rejected"
    }
    return JsonResponse({"data":data})






def send_mail_func(request):
    company = Company.objects.all().first()
    merge_data = {
        'company': company, 
        'o':None
    }
    # subject = render_to_string("email/message_subject.txt", merge_data).strip()
    # text_body = render_to_string("email/message_body.txt", merge_data)
    # html_body = render_to_string("email/message_body.html", merge_data)
    
    # msg = EmailMultiAlternatives(
    #     subject=subject, from_email="desphixs@gmail.com",
    #     to=["doctordestinyome@gmail.com"], body=text_body
    # )
    # msg.attach_alternative(html_body, "text/html")
    # msg.send()
    
    
    # return HttpResponse("Email Sent")
    return render(request, "email/message_body.html", merge_data)
    

@login_required
def vendor_payout_update(request):
    if request.user.profile.seller != True:
        messages.error(request, f"Hey {request.user.username}, you are not a vendor yet, create account now.")
        return redirect("vendor:become-vendor")
    
    vendor = Vendor.objects.get(user=request.user, profile=request.user.profile)
    if request.method == "POST":
        form = PayoutForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, "Payout Settings Saved.")
            return redirect("vendor:vendor_payout_update")
    else:
        form = PayoutForm(instance=vendor)
    context = {
        "form":form,
        "vendor":vendor,
    }    
    return render(request, "vendor/vendor_payout_update.html", context)



@login_required
def vendor_review(request):
    reviews = Review.objects.filter(product__vendor=request.user.vendor).order_by("-id")
    active_reviews = Review.objects.filter(product__vendor=request.user.vendor, active=True).order_by("-id")
    
    context = {
        "active_reviews":active_reviews,
        "reviews":reviews,
    } 
       
    return render(request, "vendor/vendor_review.html", context)


@login_required
def vendor_faq(request):
    faqs = ProductFaq.objects.filter(product__vendor=request.user.vendor).order_by("-id")
    active_faqs = ProductFaq.objects.filter(product__vendor=request.user.vendor, active=True).order_by("-id")
    
    context = {
        "active_faqs":active_faqs,
        "faqs":faqs,
    } 
       
    return render(request, "vendor/vendor_faqs.html", context)


def vendor_shop_view_page(request, vid):
    vendor = Vendor.objects.get(vid=vid, active=True)
    products = Product.objects.filter(vendor=vendor, status="published").order_by("-id")
    products_count = Product.objects.filter(vendor=vendor, status="published").order_by("-id")
    top_selling = Product.objects.filter(vendor=vendor, status="published").order_by("-orders")[:10]
    reviews = Review.objects.filter(product__vendor=vendor, active=True).order_by("-id")

    query = request.GET.get("q")
    if query:
        products = products.filter(Q(oid__icontains=query)).distinct()
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        "vendor":vendor,
        "products_count":products_count,
        "products":products,
        "top_selling":top_selling,
        "reviews":reviews,
    }    
    return render(request, "vendor/vendor_shop.html", context)


def vendor_notification(request):
    notification = Notification.objects.filter(vendor=request.user.vendor).order_by("-id")
    
    context = {
        "notification":notification,
    }    
    return render(request, "vendor/vendor_notification.html", context)
    
    
@csrf_exempt
def vendor_follow(request):
    id = request.GET['id']
    vendor = Vendor.objects.get(id=id)
    user = request.user 
    bool = False
    
    if user in vendor.followers.all():
        vendor.followers.remove(user)
        bool = False
    else:
        vendor.followers.add(user)
        bool = True
    data = {
        "bool":bool,
        "followers":vendor.followers.all().count(),
    }
    return JsonResponse({'data':data})


@csrf_exempt
def vendor_follow_2(request, id):
    
    vendor = Vendor.objects.get(id=id)
    user = request.user 
    bool = False
    
    if user in vendor.followers.all():
        vendor.followers.remove(user)
        bool = False
    else:
        vendor.followers.add(user)
        bool = True
    
    return redirect("vendor:vendor_shop_view_page", vendor.vid)
    
    
def send_reply(request):
    id = request.GET['id']
    reply = request.GET['reply']
    
    review = Review.objects.get(id=id)
    review.reply = reply
    review.save()

    data = {
        "bool": True,
    }
    
    return JsonResponse({"data":data})


def send_answer(request):
    id = request.GET['id']
    answer = request.GET['answer']
    
    faq = ProductFaq.objects.get(id=id)
    faq.answer = answer
    faq.save()

    data = {
        "bool": True,
    }
    
    return JsonResponse({"data":data})




# Messaing

@login_required
def inbox(request):
    # sender_id = request.user
    # reciever_id = User.objects.get(id=rid)
    # messagess =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id])
    
    user_id = request.user

    messagess = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")
    print("messages ======================", messagess)
    
    context = {
        'messagess': messagess,
    }
    return render(request, 'directs/my_messages.html', context)


@login_required
def get_inbox(request, username):
    # Message Detail
    sender_id = request.user
    reciever_id = User.objects.get(username=username)
    message_detail =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id]).order_by("date")
    
    
    
    user_id = request.user
    message_list = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__reciever=user_id) |
                Q(reciever__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),reciever=user_id) |
                        Q(reciever=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")
    

    
    context = {
        'message_detail': message_detail,
        'message_list': message_list,
        'reciever_id': reciever_id,
    }
    return render(request, 'directs/inbox_messages.html', context)
    

# def get_messages_ajax(request, username):
#     sender_id = request.user
#     reciever_id = User.objects.get(username=username)
#     message_detail =  ChatMessage.objects.filter(sender__in=[sender_id, reciever_id], reciever__in=[sender_id, reciever_id]).order_by("date")
    
    
#     jsonData = serializers.serialize('json', message_detail)
#     return JsonResponse({'data':jsonData})


def send_message_ajax(request, username):
    sender_id = request.user
    reciever_id = User.objects.get(username=username)
    messages = request.GET.get("messagee")
    message =  ChatMessage.objects.create(user=request.user, sender=sender_id, reciever=reciever_id, message=messages)
    message.save()
    
    context = {
        "bool":True
    }
    
    return JsonResponse({'data':context})



@login_required
def search_users(request):
    users = User.objects.all()

    query = request.GET.get("q")
    if query:
        users = users.filter(Q(username__icontains=query)|Q(full_name__icontains=query)).distinct()
        
            
    context = {
        'query': query,
        'users': users,
    }
    return render(request, 'directs/search_user.html', context)


def onboard_seller():
    url = "https://api.paypal.com/v1/customer/partners/merchant-integrations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <Access-Token>"
    }
    data = {
        "partner_merchant_external_id": "<External-ID>",
        "partner_merchant_industry": "<Industry>",
        "partner_merchant_onboarding_type": "<Onboarding-Type>",
        "partner_merchant_product_name": "<Product-Name>",
        "partner_merchant_redirect_urls": {
            "return_url": "<Return-URL>",
            "cancel_url": "<Cancel-URL>"
        },
        "partner_merchant_partner_logo_url": "<Logo-URL>",
        "partner_merchant_legal_consents": [
            {
                "type": "<Consent-Type>",
                "granted": True,
                "granted_time": "<Consent-Time>"
            }
        ],
        "partner_merchant_details": {
            "business_info": {
                "business_name": "<Business-Name>",
                "business_address": {
                    "line1": "<Line-1>",
                    "line2": "<Line-2>",
                    "city": "<City>",
                    "state": "<State>",
                    "postal_code": "<Postal-Code>",
                    "country_code": "<Country-Code>"
                },
                "business_phone": {
                    "country_code": "<Country-Code>",
                    "national_number": "<National-Number>"
                },
                "business_email_address": "<Email-Address>"
            },
            "owner_info_list": [
                {
                    "owner_type": "<Owner-Type>",
                    "owner_name_info": {
                        "first_name": "<First-Name>",
                        "last_name": "<Last-Name>"
                    },
                    "owner_address_info_list": [
                        {
                            "address_info_type": "<Address-Type>",
                            "address_info_value_list": [
                                "<Line-1>", 
                                "<Line-2>", 
                                "<City>", 
                                "<State>", 
                                "<Postal-Code>", 
                                "<Country-Code>"
                            ]
                        }
                    ],
                    "owner_email_address_list":[
                        {
                            "email_address_type":"<Email-Type>",
                            "email_address_value":"<Email-Address>"
                        }
                    ],
                    "owner_phone_info_list":[
                        {
                            "phone_info_type":"<Phone-Type>",
                            "phone_info_value":{
                                "country_code":"<Country-Code>",
                                "national_number":"<National-Number>"
                            }
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()



# import requests

# def onboard_seller():
#     url = "https://api.paypal.com/v1/customer/partners/merchant-integrations"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer <Access-Token>"
#     }
#     data = {
#         "partner_merchant_external_id": "<External-ID>",
#         "partner_merchant_industry": "<Industry>",
#         "partner_merchant_onboarding_type": "<Onboarding-Type>",
#         "partner_merchant_product_name": "<Product-Name>",
#         "partner_merchant_redirect_urls": {
#             "return_url": "<Return-URL>",
#             "cancel_url": "<Cancel-URL>"
#         },
#         "partner_merchant_partner_logo_url": "<Logo-URL>",
#         "partner_merchant_legal_consents": [
#             {
#                 "type": "<Consent-Type>",
#                 "granted": True,
#                 "granted_time": "<Consent-Time>"
#             }
#         ],
#         "partner_merchant_details": {
#             "business_info": {
#                 "business_name": "<Business-Name>",
#                 "business_address": {
#                     "line1": "<Line-1>",
#                     "line2": "<Line-2>",
#                     "city": "<City>",
#                     "state": "<State>",
#                     "postal_code": "<Postal-Code>",
#                     "country_code": "<Country-Code>"
#                 },
#                 "business_phone": {
#                     "country_code": "<Country-Code>",
#                     "national_number": "<National-Number>"
#                 },
#                 "business_email_address": "<Email-Address>"
#             },
#             "owner_info_list": [
#                 {
#                     "owner_type": "<Owner-Type>",
#                     "owner_name_info": {
#                         "first_name": "<First-Name>",
#                         "last_name": "<Last-Name>"
#                     },
#                     "owner_address_info_list": [
#                         {
#                             "address_info_type": "<Address-Type>",
#                             "address_info_value_list": [
#                                 "<Line-1>", 
#                                 "<Line-2>", 
#                                 "<City>", 
#                                 "<State>", 
#                                 "<Postal-Code>", 
#                                 "<Country-Code>"
#                             ]
#                         }
#                     ],
#                     "owner_email_address_list":[
#                         {
#                             "email_address_type":"<Email-Type>",
#                             "email_address_value":"<Email-Address>"
#                         }
#                     ],
#                     "owner_phone_info_list":[
#                         {
#                             "phone_info_type":"<Phone-Type>",
#                             "phone_info_value":{
#                                 "country_code":"<Country-Code>",
#                                 "national_number":"<National-Number>"
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     }

#     response = requests.post(url, headers=headers, json=data)
#     return response.json()



from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests

def onboard_seller_view(request):
    # Your PayPal partner ID and redirect URL
    partner_id = "EUKJWPKTHT5C2"
    redirect_url = "vendor:dashboard"

    # Generate a unique referral link for the seller
    referral_link = f"https://www.paypal.com/us/webapps/mpp/referral/paypal-partner-referral-program?partner_id={partner_id}&amp;utm_campaign=Referral&amp;utm_medium=Link&amp;utm_source=PPReferral&view=web"

    # Create a PayPal Partner Referral API request to track the referral
    payload = {
        "partner_id": partner_id,
        # "campaign_id": "YOUR_CAMPAIGN_ID",
        "merchant_id": "EUKJWPKTHT5C2",
        "redirect_uri": redirect_url
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer A21AAJnuaq4pYdg80lOwOcK0n7IJh-232cSuBY7Jklc3rFOSaSIz8iCRJaPtUxxb-oi-S3ERkofsxhyWx5uWq6JPBfnRzTMdw"
    }
    response = requests.post("https://api.paypal.com/v1/customer/partner-referrals", json=payload, headers=headers)

    # Redirect the seller to the referral link
    return HttpResponseRedirect(referral_link)






# def onboard_seller_view_2(request):
#     # Retrieve seller's information from the request
#     seller_name = request.POST.get('name')
#     seller_email = request.POST.get('email')
#     # Call PayPal's Partner Referral API to retrieve the redirect URL
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer A21AAJnuaq4pYdg80lOwOcK0n7IJh-232cSuBY7Jklc3rFOSaSIz8iCRJaPtUxxb-oi-S3ERkofsxhyWx5uWq6JPBfnRzTMdw'
#     }
#     data = {
#         'operation': 'API_INTEGRATION',
#         'productIntentId': 'PAYMENT',
#         'partnerConfiguration': {
#             'partnerId': 'EUKJWPKTHT5C2',
#             'features': ['PAYMENT', 'REFERRAL'],
#             'integrationMethod': 'PAYPAL'
#         },
#         'collectedConsent': {
#             'trackingId': 'wrweijweirnemdfioweworuwer',
#             'consentShared': True
#         },
#         'webExperience': {
#             'partnerLogoUrl': 'https://img.freepik.com/free-vector/gradient-quill-pen-design-template_23-2149837194.jpg?w=2000',
#             'userExperienceFlow': 'FULL',
#             'returnUrl': '/vendor/vendor_payout_update/',
#             'returnUrlDescription': 'Return to seller dashboard'
#         },
#         'partnerLogoUrl': 'https://img.freepik.com/free-vector/gradient-quill-pen-design-template_23-2149837194.jpg?w=2000',
        
#         'accountInfo': {
#             'emailAddress': seller_email,
#             'name': {
#                 'givenName': seller_name.split()[0],
#                 'surname': seller_name.split()[-1]
#             }
#         }
#     }
#     response = requests.post('https://api.paypal.com/v1/partner-referrals/referral/', headers=headers, json=data)
#     # Redirect the seller to PayPal's onboarding flow
    
#     return redirect(response.json()['links'][0]['href'])


import requests

def onboard_seller_view_2(request):
    # PayPal API endpoint
    url = 'https://api-m.sandbox.paypal.com/v2/customer/partner-referrals'

    # PayPal access token
    access_token = 'A21AAJnuaq4pYdg80lOwOcK0n7IJh-232cSuBY7Jklc3rFOSaSIz8iCRJaPtUxxb-oi-S3ERkofsxhyWx5uWq6JPBfnRzTMdw'

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Request data
    data = {
        'partner_config_override': {
            'partner_logo_url': 'https://yourpartnerlogo.com',
            'return_url': 'https://yourpartnerreturnurl.com',
            'action_url': 'https://yourpartneractionurl.com'
        },
        'campaign_code': 'wekjweijfiwnefjwfiowejfw',
        'customer_info': {
            'email_address': request.user.email,
            'first_name': request.user.username,
            'last_name': request.user.username
        }
    }
    

    # Send request to PayPal API
    response = requests.post(url, headers=headers, json=data)

    # If request is successful, return the onboarding link
    if response.status_code == 201:
        return response.json()['links'][0]['href']
    else:
        # If request is unsuccessful, raise an exception with the error message
        raise Exception(response.json()['message'])

def generate_paypal_access_token():
    url = 'https://api.paypal.com/v1/oauth2/token'
    client_id = settings.PAYPAL_CLIENT_ID
    secret = settings.PAYPAL_SECRET_ID

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }

    data = {
        'grant_type': 'client_credentials'
    }

    auth = (client_id, secret)

    response = requests.post(url, headers=headers, data=data, auth=auth)

    if response.status_code == 200:
        print("Access TOken =============", response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(response.json()['error_description'])






def calculate_monthly_revenue(month, year):
    # Convert month and year to datetime object
    start_date = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end_date = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    
    # Calculate the revenue for the specified month
    revenue = CartOrder.objects.filter(date__gte=start_date, date__lt=end_date).aggregate(total_revenue=Sum('total'))['total_revenue']
    
    return revenue or 0

def list_yearly_revenue(year):
    revenue_by_month = []
    
    for month in range(1, 13):
        revenue = calculate_monthly_revenue(month, year)
        revenue_by_month.append((month, revenue))
    
    return revenue_by_month


def revenue_summary(request):
    year = 2023  # Change this to the desired year
    revenue_by_month = list_yearly_revenue(year)
    
    context = {
        'revenue_by_month': revenue_by_month
    }
    
    return render(request, 'vendor/revenue_summary.html', context)