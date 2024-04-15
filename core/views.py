from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import OuterRef, Subquery, Q, Count, Sum, F, FloatField
from django.core.paginator import Paginator
from django.db.models.functions import ExtractMonth, ExtractYear

import calendar

from addons.models import BasicAddon, Company
from userauths.forms import UserUpdateForm, ProfileUpdateForm
from store.forms import AddressForm, BillingAddressForm
from core.models import BillingAddress, Wishlist, Address
from store.models import CartOrder, CartOrderItem, Product, ProductBidders, ProductOffers
from userauths.models import Profile, User
from vendor.models import ChatMessage


@login_required
def buyer_account(request):

    output = CartOrder.objects.filter(buyer=request.user, payment_status="paid").annotate(month=ExtractMonth("date")).values("month").annotate(count=Count("id"),).order_by("month")
    
    monthNumber=[]
    totalOrders=[]
    


    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])

    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f"Profile updated successfully. ")
            return redirect('core:buyer-dashboard')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
        "monthNumber":monthNumber,
        "totalOrders":totalOrders,
    }
    return render(request, 'buyer/dashboard.html', context)

@login_required
def buyer_profile(request):

    profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f"Profile updated successfully. ")
            return redirect('core:profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'profile': profile,
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'buyer/buyer_profile.html', context)


@login_required
def buyer_profile_settings(request):

    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f"Profile updated successfully. ")
            return redirect('core:buyer-dashboard')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'buyer/buyer_profile_settings.html', context)


@login_required
def buyer_orders(request):
    orders = CartOrder.objects.filter(buyer=request.user).order_by("-id")
    orders_count = CartOrder.objects.filter(buyer=request.user).order_by("-id")
    shipped = CartOrder.objects.filter(buyer=request.user, delivery_status="shipped").order_by("-id")
    collected = CartOrder.objects.filter(buyer=request.user, delivery_status="collected").order_by("-id")
    
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'orders':orders,
        'orders_count':orders_count,
        'shipped':shipped,
        'collected':collected,
    }
    
    return render(request, 'buyer/orders.html', context)

@login_required
def buyer_order_detail(request, oid):
    order = CartOrder.objects.get(oid=oid, buyer=request.user)
    products = CartOrderItem.objects.filter(order=order).order_by("-id")

    context = {
        'order':order,
        'products':products,
    }
    return render(request, 'buyer/order-detail.html', context)


@login_required
def buyer_address(request):
    address = Address.objects.filter(user=request.user).order_by("-id")
    billing_address = BillingAddress.objects.filter(user=request.user).order_by("-id")

    form = AddressForm()
    billing_form = BillingAddressForm()

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "New Address Added Successfully.")
            return redirect("core:buyer-address")

    

    context = {
        'address':address,
        'form':form,
        'billing_form':billing_form,
        'billing_address':billing_address,
    }
    return render(request, 'buyer/address.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


def add_billing_address(request):
    if request.method == "POST":
        billing_form = BillingAddressForm(request.POST)
        if billing_form.is_valid():
            new_billing_form = billing_form.save(commit=False)
            new_billing_form.user = request.user
            new_billing_form.save()
            messages.success(request, "New Billing Address Added Successfully.")
            return redirect("core:buyer-address")
    
    return redirect("core:buyer-address")
        
@login_required
def buyer_edit_address(request, id):
    address = Address.objects.get(user=request.user, id=id)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Address updated successfully.")
            return redirect("core:buyer-address")
    else:
        form = AddressForm(instance=address)
    
    context = {
        'form':form,
    }
    return render(request, 'buyer/address-edit.html', context)


@login_required
def buyer_delete_address(request, id):
    address = Address.objects.get(user=request.user, id=id)
    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect("core:buyer-address")

@login_required
def buyer_delete_billing_address(request, id):
    address = BillingAddress.objects.get(user=request.user, id=id)
    address.delete()
    messages.success(request, "Billing Address deleted successfully.")
    return redirect("core:buyer-address")


@login_required
def buyer_billing_address(request):
    address = BillingAddress.objects.filter(user=request.user).order_by("-id")

    form = BillingAddressForm()

    if request.method == "POST":
        form = BillingAddressForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "New Billing Address Added Successfully.")
            return redirect("core:buyer-billing-address")

    context = {
        'address':address,
        'form':form,
    }
    return render(request, 'buyer/billing-address.html', context)


def make_billing_address_default(request):
    id = request.GET['id']
    BillingAddress.objects.update(status=False)
    BillingAddress.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def buyer_edit_billing_address(request, id):
    address = BillingAddress.objects.get(user=request.user, id=id)

    if request.method == "POST":
        form = BillingAddressForm(request.POST, instance=address)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Billing Address updated successfully.")
            return redirect("core:buyer-address")
    else:
        form = BillingAddressForm(instance=address)
    
    context = {
        'form':form,
    }
    return render(request, 'buyer/billing-address-edit.html', context)

@login_required
def buyer_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist':wishlist,
    }
    return render(request, 'buyer/wishlist.html', context)

@login_required
def delete_from_wishlist(request, id):
    wishlist = Wishlist.objects.get(user=request.user, id=id)
    wishlist.delete()
    messages.success(request, "Product removed from wishlist")
    return redirect("core:buyer-wishlist")

def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    context = {}
    login_bool = False
    bool = None

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
        print(wishlist_count)

        login_bool = True
        if wishlist_count > 0: 
            bool = False
        else:
            new_wishlist = Wishlist.objects.create(user=request.user,product=product)
            new_wishlist.save()
            bool = True

    else:
        login_bool = False
    data = {
        "bool":bool,
        "login_bool":login_bool,
    }
    return JsonResponse({"data":data})

@login_required
def buyer_invoices(request):
    invoices = CartOrder.objects.filter(buyer=request.user, payment_status="paid")
    context = {
        'invoices':invoices,
    }
    return render(request, 'buyer/invoices.html', context)

def buyer_invoice_detail(request, oid):
    invoice = CartOrder.objects.get(payment_status="paid", oid=oid)
    items = CartOrderItem.objects.filter(order=invoice)

    context = {
        'invoice':invoice,
        'items':items,
    }
    return render(request, 'buyer/invoice-detail.html', context)

def buyer_track_order(request):
    if request.method == "POST":
        try:
            order_id = request.POST.get("order_id")
            order = CartOrder.objects.get(oid=order_id, payment_status="paid")
            messages.success(request, "Order Found")
            return redirect("core:tracked-order", order.oid)
        except:
            messages.error(request, "Order matching ID does not exist, make sure ID number is correct.")
            return redirect("core:order-tracker")
       
            
            
    return render(request, 'buyer/order-tracker.html')

def tracked_order(request, oid):
    try:
        order = CartOrder.objects.get(oid=oid, payment_status="paid")
        order_items = CartOrderItem.objects.filter(order=order)
    except:
        messages.error(request, "Order matching ID does not exist, make sure ID number is correct.")
        return redirect("core:order-tracker")
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'buyer/tracked-order.html', context)

@login_required
def buyer_bids(request):
    bids = ProductBidders.objects.filter(user=request.user).order_by("-id")
    won_bids = ProductBidders.objects.filter(user=request.user, winner=True, product__bidding_ended=True).order_by("-id")
    lost_bids = ProductBidders.objects.filter(user=request.user, winner=False, product__bidding_ended=True).order_by("-id")
    
    context = {
        'bids': bids,
        'won_bids': won_bids,
        'lost_bids': lost_bids,
    }
    return render(request, 'buyer/buyer-bids.html', context)


@login_required
def buyer_bids_detail(request, pid, bid):
    product = Product.objects.get(pid=pid)
    bid = ProductBidders.objects.get(user=request.user, bid=bid, product=product)
    if bid.winner == False:
        messages.error(request, f"You cannot view this bid")
        return redirect("core:buyer_bids")
    
    others = ProductBidders.objects.filter(product=product).order_by("-price")
    context = {
        'bid': bid,
        'product': product,
        'others': others,
    }
    return render(request, 'buyer/buyer-bids-detail.html', context)

@login_required
def buyer_offer(request):
    offer = ProductOffers.objects.filter(user=request.user)
    accepted_offer = ProductOffers.objects.filter(user=request.user, status="accept")
    rejected_offer = ProductOffers.objects.filter(user=request.user, status="reject")
    
    context = {
        'offer': offer,
        'accepted_offer': accepted_offer,
        'rejected_offer': rejected_offer,
    }
    return render(request, 'buyer/buyer-offer.html', context)

@login_required
def buyer_offer_detail(request, pid, oid):
    product = Product.objects.get(pid=pid)
    offer = ProductOffers.objects.get(user=request.user, oid=oid)

    context = {
        'offer': offer,
        'product': product,
    }
    return render(request, 'buyer/buyer-offer-detail.html', context)


def cancel_order(request, oid):
    order = CartOrder.objects.get(oid=oid, payment_status="paid")
    orderitems = CartOrderItem.objects.filter(order=order)
    
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'buyer/buyer-cancel-order.html', context)




def cancel_orderitem(request):
    id = request.GET['id']
    orderitem = CartOrderItem.objects.get(id=id)
    orderitem.cancelled = True
    orderitem.save()
    
    # Email ======================
    basic_addon = BasicAddon.objects.all().first()
    if basic_addon.send_email_notifications == True:
    
        company = Company.objects.all().first()
        merge_data = {
            'company': company, 
            'orderitem': orderitem, 
        }
        subject = f"Order Item Cancelled for {orderitem.product_obj.title}"
        text_body = render_to_string("email/message_body.txt", merge_data)
        html_body = render_to_string("email/orderitem_cancelled.html", merge_data)
        
        msg = EmailMultiAlternatives(
            subject=subject, from_email=settings.FROM_EMAIL,
            to=[orderitem.vendor.shop_email], body=text_body
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
    # Email ==========================
    
    data = {
        'bool': True,
        'message': "Order Cancelled",
    }
    return JsonResponse({"data":data})





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
    return render(request, 'buyer/messages.html', context)


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
    return render(request, 'buyer/inbox_messages.html', context)
    


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
    return render(request, 'buyer/search_user.html', context)
    
        
        
