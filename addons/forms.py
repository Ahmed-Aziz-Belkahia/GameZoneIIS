from django import forms
from addons.models import BasicAddon, Company, EarningPoints, NewsLetter, Policy, TaxRate, SuperUserSignUpPin, ContactUs, FAQs, Announcements, PlatformNotifications, TutorialVideo

class ContactUSForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Full Name'}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Email'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Subject'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': "", 'placeholder':'Message'}), required=True)

    class Meta:
        model = ContactUs
        fields = ['full_name','subject','email','topic','message']