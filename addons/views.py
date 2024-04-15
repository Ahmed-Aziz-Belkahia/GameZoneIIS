from django.shortcuts import render, redirect
from addons.models import BasicAddon, Company, EarningPoints, NewsLetter, Policy, TaxRate, SuperUserSignUpPin, ContactUs, FAQs, Announcements, PlatformNotifications, TutorialVideo
from addons.forms import ContactUSForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.http import JsonResponse



def contact_us(request):
    
    if request.method == "POST":
        form = ContactUSForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You message have been sent, an agent would would contact you soon.')
            return redirect("addons:contact_us")
    
    else:
        form = ContactUSForm()
    
    context = {
        "form":form,
    }
        
    return render(request, "addons/contact_us.html", context)
            
    
    
def send_faq_qs(request):
    question = request.POST.get("question")
    email = request.POST.get("email")
    FAQs.objects.create(question=question,email=email,)
    data = {
        "message":"Question sent successfully, would be answered soon."
    }
    return JsonResponse({"data":data})


def subscribe_to_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and is_valid_email(email):
            try:
                # Attempt to retrieve the newsletter object by email
                newsLetter = NewsLetter.objects.get(email=email)
            except ObjectDoesNotExist:
                # If the newsletter object does not exist, create a new one
                newsLetter = NewsLetter.objects.create(email=email)
            
            # Prepare data to be sent in the JsonResponse
            data = {
                "id": newsLetter.id,
                "message": "Thanks for subscribing to our newsletter.",
            }
        else: 
            data = {
                "message": "enter a valid email.",
            }
        return JsonResponse({"data": data})
    else:
        # If the request method is not POST, return a JsonResponse with an error message
        return JsonResponse({"error": "Invalid request method. Must be a POST request."})

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def privacy_policy(request):
    try:
        policy = Policy.objects.all().first()
    except:
        policy = None
    context = {
        "policy":policy,
    }
        
    return render(request, "addons/privacy_terms_condition.html", context)

def terms_and_conditions(request):
    try:
        policy = Policy.objects.all().first()
    except:
        policy = None
    context = {
        "policy":policy,
    }
        
    return render(request, "addons/terms_and_conditions.html", context)

def return_policy(request):
    try:
        policy = Policy.objects.all().first()
    except:
        policy = None
    context = {
        "policy":policy,
    }
        
    return render(request, "addons/return_policy.html", context)

def secure_purchases(request):
    try:
        policy = Policy.objects.all().first()
    except:
        policy = None
    context = {
        "policy":policy,
    }
        
    return render(request, "addons/secure_purchases.html", context)


def about_us(request):
    company = Company.objects.all().first()
    
    context = {
        "company":company,
    }
        
    return render(request, "addons/about_us.html", context)