from django import forms
import phonenumbers
import random
import string
from .models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginForm(forms.Form):

    phone_number = forms.CharField(
        label="Enter your number", 
        initial='+7',
        widget=forms.TextInput(attrs={
            'type': 'tel'  
        })
    )

class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="код",
        max_length=4,
        min_length=4,
        widget=forms.TextInput(attrs={'type': 'number'}) 
    )
        

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return HttpResponseRedirect(reverse("referral:login"))  
        return func(request, *args, **kwargs)  
    return wrapper

def auth_code_required(func):
    def wrapper(request, *args, **kwargs):
        if not (request.session.get('auth_code') and request.session.get('phone_number')):
            return HttpResponseRedirect(reverse("referral:login"))  
        return func(request, *args, **kwargs)  
    return wrapper

def validate_number(number):
    try:
        info = {
            'message': None,
            'formatted_number': None
        }
        
        parsed_number = phonenumbers.parse(number, "RU")
        if phonenumbers.region_code_for_number(parsed_number) != "RU" or not phonenumbers.is_valid_number(parsed_number):
            info['message'] = "Invalid phone number"
        else:
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            info['formatted_number'] = formatted_number 
    except phonenumbers.NumberParseException:
        info['message'] = "Invalid format of phone number"

    return info

def send_code(phone_number):
    code = '1234'
    return code

    
def generate_unique_code(length=6):
    characters = string.ascii_letters + string.digits  

    max_attempts = 1000
    attempt = 0

    while(attempt < max_attempts):
        invite_code = ''.join(random.choices(characters, k=length))
        if not User.objects.filter(invite_code=invite_code).exists():
            return invite_code
        attempt += 1
    
    return None



