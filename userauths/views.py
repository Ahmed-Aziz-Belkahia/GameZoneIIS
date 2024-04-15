from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect

import urllib.parse
from datetime import timedelta

from addons.models import Company, EarningPoints, NewsLetter
from userauths.models import Profile, User
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm



def Register(request, *args, **kwargs):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return redirect('store:home')   
    try:
        earning_point = EarningPoints.objects.get()
    except:
        earning_point = None

    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=password)
        login(request, user)

        NewsLetter.objects.create(email=username)
        messages.success(request, f"Hi {request.user.username}, your account was created successfully.")

        try:
            profile = Profile.objects.get(user=request.user)
            profile.wallet += earning_point.signup_point
            profile.save()
        except:
            profile = Profile.objects.get(user=request.user)
            profile.wallet += 1
            profile.save()

        return redirect('store:home')
    
    context = {'form':form}
    return render(request, 'userauths/sign-up.html', context)


def loginView(request):

    # if request.user.is_authenticated:
    #     return redirect('core:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                # return HttpResponseRedirect(request.GET['next'])
                return redirect('store:home')
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return HttpResponseRedirect("/")


def loginViewTemp(request):
    # messages.success(request, f"Login for better experience.")
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('store:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                # return redirect()
                next_url = request.GET.get("next", 'store:home')
                return redirect(next_url)
                
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return render(request, "userauths/sign-in.html")



def loginAsVendor(request):
    # messages.success(request, f"Login for better experience.")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                return redirect('vendor:dashboard')
                    
                    # return HttpResponseRedirect(request.GET['next'])
                # if request.GET['next']:
                # else:
                #     return redirect('store:home')
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return render(request, "userauths/vendor-sign-in.html")


def logoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("userauths:sign-in")



@login_required
def ProfileUpdate(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'userauths/profile-update.html', context)


def error404View(request):
    return render(request, 'base/404.html')

def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('Referer Profile:', profile.id)
    except:
        pass
    print("Session Expiry Date:" + str(request.session.get_expiry_age()))
    return render(request, 'core/main.html', {})

@login_required
def my_referrals(request):
    try:
        company = CompanyDetail.objects.get()
    except:
        company = None
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommened_profiles()
    active_refs = Profile.objects.filter(active=True, recommended_by=request.user)
    all_refs = Profile.objects.filter(recommended_by=request.user)
    ref_content = ReferralMessage.objects.get()
    content_string = urllib.parse.quote_plus(ref_content.content)
    title_string = urllib.parse.quote_plus(ref_content.title)
    url_string = f"{company.website_address}/user/sign-up/{request.user.profile.code}"

    my_recomended = Profile.objects.filter(recommended_by=request.user).values_list('user__id', flat=True)
    second_level_recommended=Profile.objects.filter(recommended_by__in=my_recomended)


    context = {
            'second_level_recommended': second_level_recommended,
            'url_string': url_string,
            'title_string': title_string,
            'content_string': content_string,
            'ref_content': ref_content,
            'my_recs': my_recs,
            'active_refs': active_refs,
            'all_refs': all_refs,
        }
    return render(request, 'core/referrals.html', context)


@login_required
def profile_settings(request):
    transaction_details = TransactionDetails.objects.filter(purchased_package__user=request.user)
    # user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = userUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f"Hi {request.user.username}, your profile have been updated.")
            return redirect('userauths:profile-setting')
    else:
        p_form = profileUpdateForm(instance=request.user.profile)
        u_form = userUpdateForm(instance=request.user)
    
    context = {
            "transaction_details":transaction_details,
            'profile': profile,
            'p_form': p_form,
            'u_form': u_form,
        }
    return render(request, "core/profile-settings.html", context)

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        

        user = request.user
        profile = request.user.profile


        try:
            company = CompanyDetail.objects.get()
        except:
            company = None
        
        url_string = f"{company.website_address}/user/sign-up/{request.user.profile.code}"
    
        context = {
            'url_string':url_string,
            'profile':profile,
    }
    else:
        
        profile = Profile.objects.get(user=request.user)
        
        context = {
            'profile': profile,
            
        }
    return render(request, 'userauths/user-profile-detail.html', context)



def check_email(request):
    return render(request, 'userauths/password-reset/check_email.html')
    