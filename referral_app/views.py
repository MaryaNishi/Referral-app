from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import time
from .models import User
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializer import UserPhoneNumbersSerializer


from referral_app.helper import LoginForm, VerifyCodeForm, validate_number, send_code, generate_unique_code, login_required, auth_code_required

@csrf_exempt
@api_view(['POST'])
def check_invite_code(request):
    invite_code = request.data.get('invite_code')
    if invite_code and User.objects.filter(invite_code=invite_code).exclude(id=request.session['user_id']).exists():
        return Response({"valid": True})
    return Response({"valid": False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_phone_numbers(request):
    current_user = User.objects.get(id=request.session['user_id'])
    users = User.objects.filter(activated_invite_code=current_user.invite_code)
    serializer = UserPhoneNumbersSerializer(users, many=True)
    return Response(serializer.data)


@auth_code_required
def get_authentication(request):
    if request.method == "POST":

        form = VerifyCodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']

            if code == request.session['auth_code']:
                return HttpResponseRedirect(reverse("referral:login_user"))
            

        message = "Неверный код. Попробуйте снова."
        print(message)
        return render(request, "referral_app/authentication.html", {
            "form": form,
            "phone_number": request.session['phone_number'],
            "message": message
        })
        
    return HttpResponseRedirect(reverse("referral:login"))


@auth_code_required
def login_user(request):
    try:
        user = User.objects.get(phone_number=request.session['phone_number'])
    except User.DoesNotExist:
        invite_code = generate_unique_code()
        if not invite_code:
            message = "Код, к сожалению, не был сгенерирован. Попробуйте снова."
            return render(request, "referral_app/login.html", {
                "form": LoginForm(),
                "message": message
            })
        
        user = User(phone_number=request.session['phone_number'], invite_code=invite_code)
        user.save()
    except Exception as e:
        message = f'Ошибка при авторизации пользователя: {e}'
        print(message)

        return render(request, "referral_app/login.html", {
            "form": LoginForm(),
            "message": message
        })



    request.session['user_id'] = user.id
    request.session['auth_code'] = None
    print('Пользователь успешно авторизовался')
    return HttpResponseRedirect(reverse("referral:profile"))


@login_required
def profile_view(request):
    message = ''
    if request.method == "POST":
        invite_code = request.POST.get('invite-code')
        if invite_code:
            user = User.objects.get(phone_number=request.session['phone_number'])
            user.activated_invite_code = invite_code
            user.save()
        else:
            message = 'Invalid invite code'


    return render(request, "referral_app/profile.html", {
        "number": request.session['phone_number'],
        "activated_invite_code": User.objects.get(phone_number=request.session['phone_number']).activated_invite_code,
        "message": message
    })


def login_view(request):

    request.session['user_id'] = None

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['phone_number']
            info = validate_number(number)
            
            if info['message']:
                print(info['message'])

                return render(request, "referral_app/login.html", {
                    "form": form,
                    "message": info['message']
                })
            
            time.sleep(2)
            request.session['phone_number'] = info['formatted_number']
            request.session['auth_code'] = send_code(number)
            
            return render(request, "referral_app/authentication.html", {
                "form": VerifyCodeForm(),
                "phone_number": request.session['phone_number']
            })
        else:
            message = 'Неверная форма. Пожалуйста, попробуйте снова.'
            print(message )
            return render(request, "referral_app/login.html", {
                    "form": form,
                    "message": message 
                })
            
            
    return render(request, "referral_app/login.html", {
        "form": LoginForm()
    })



def logout_view(request):
    request.session['user_id'] = None
    return HttpResponseRedirect(reverse("referral:login"))