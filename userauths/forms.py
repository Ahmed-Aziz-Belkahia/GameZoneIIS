from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from django.forms import ImageField, FileInput
from django.contrib.auth import get_user_model
# from captcha.fields import CaptchaField


class DateInput(forms.DateInput):
    input_type = "date"

class StaffCreationForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = "__all__"
        widgets = {
            'date_joined': DateInput(),
            'last_login': DateInput(),
        }

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Full Name'}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': "", 'placeholder':'Username'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control' , 'id': "", 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'btn__btn__btn form-control' , 'id': "", 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'btn__btn__btn form-control' , 'id': "", 'placeholder':'Confirm Password'}), required=True)
    # captcha=CaptchaField()
    
    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']
       
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Full Name', 'class': 'form-control', 'id': ""}), max_length=1000, required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Residential Address', 'class': 'form-control', 'id': ""}), max_length=1000, required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control', 'id': ""}), max_length=1000, required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'State', 'class': 'form-control', 'id': ""}), max_length=1000, required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'id': ""}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile Number', 'class': 'form-control', 'id': ""}), max_length=1000, required=False)
    image = ImageField(widget=FileInput)
    
    class Meta:
        model = Profile
        fields = ['full_name', 'image' ,'gender','address', 'city' , 'state', 'country' , 'phone' ]
        widgets = {
            'image': FileInput(attrs={'id': 'loadFile(event)'}),
            'identity_image': FileInput(attrs={'id': 'preview_id()'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']
