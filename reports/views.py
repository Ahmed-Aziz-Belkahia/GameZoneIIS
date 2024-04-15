from django.shortcuts import render, redirect
from addons.models import BasicAddon, Company
from store.models import CartOrderItem, Product,  ProductOffers, ProductBidders, Vendor
from reports.models import ProductReport, BiddingUserReport, OrderItemReport, VendoReport, GeneralIssue, OfferUserReport
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings

def report_bidding_user(request, bid):
    company = Company.objects.all().first()
    bidder = ProductBidders.objects.get(bid=bid)
    basic_addon = BasicAddon.objects.all().first()
    
    if request.method == "POST":
        message = request.POST.get("message")
        vendor = request.user.vendor
        
        report = BiddingUserReport.objects.create(
            message=message,
            vendor=vendor,
            product_bidding=bidder,
            user=bidder.user
        )
        messages.success(request, "Bidder have been reported, action would be taken immediately.")
        
        # Email ======================
        if basic_addon.send_email_notifications == True:
            merge_data = {
                'company': company, 
                'bidder': bidder, 
                'report':report,
                'message':message,
            }
            subject = f"REPORT!! A bidder have been reported"
            text_body = render_to_string("email/message_body.txt", merge_data)
            html_body = render_to_string("email/bidder_report.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject, from_email=settings.FROM_EMAIL,
                to=[company.email], body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        # Email ==========================
        return redirect("vendor:product_bidding_detail", bidder.product.pid)
    context = {
        "bidder":bidder,
    }
    return render(request, "report/report_bidder.html", context)
    


def report_offer_user(request, oid):
    company = Company.objects.all().first()
    offer = ProductOffers.objects.get(oid=oid)
    basic_addon = BasicAddon.objects.all().first()
    
    if request.method == "POST":
        message = request.POST.get("message")
        vendor = request.user.vendor
        
        report = OfferUserReport.objects.create(
            message=message,
            vendor=vendor,
            product_offer=offer,
            user=offer.user
        )
        messages.success(request, "User have been reported, action would be taken immediately.")
        
        # Email ======================
        if basic_addon.send_email_notifications == True:
            merge_data = {
                'company': company, 
                'bidder': offer, 
                'report':report,
                'message':message,
            }
            subject = f"REPORT!! A user have been reported"
            text_body = render_to_string("email/message_body.txt", merge_data)
            html_body = render_to_string("email/bidder_report.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject, from_email=settings.FROM_EMAIL,
                to=[company.email], body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        # Email ==========================
        return redirect("vendor:product_bidding_detail", bidder.product.pid)
    context = {
        "bidder":offer,
    }
    return render(request, "report/report_offer.html", context)
    




def report_product(request, pid):
    company = Company.objects.all().first()
    basic_addon = BasicAddon.objects.all().first()
    product = Product.objects.get(pid=pid)
    
    if request.method == "POST":
        message = request.POST.get("message")
        
        report = ProductReport.objects.create(
            message=message,
            product=product,
            vendor=product.vendor,
            user=request.user
        )
        messages.success(request, "You have reported this product, action would be taken immediately.")
        
        # Email ======================
        if basic_addon.send_email_notifications == True:
            merge_data = {
                'company': company, 
                'product': product, 
                'report':report,
                'message':message,
            }
            subject = f"REPORT!! A Product Was Reported"
            text_body = render_to_string("email/message_body.txt", merge_data)
            html_body = render_to_string("email/product_report.html", merge_data)
            
            msg = EmailMultiAlternatives(
                subject=subject, from_email=settings.FROM_EMAIL,
                to=[company.email], body=text_body
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        # Email ==========================
        return redirect("store:product-detail", product.pid)
    context = {
        "product":product,
    }
    return render(request, "report/report_product.html", context)
    




def report_issue(request):
    
    if request.method == "POST":
        message = request.POST.get("message")
        
        report = GeneralIssue.objects.create(
            message=message,
            user=request.user
        )
        messages.success(request, "Your issue have been reported, we would get back to you as soon as possible.")
        return redirect("core:buyer-dashboard")
    
    return render(request, "report/report-issue.html")
    


