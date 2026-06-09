from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

import json
import random
import time

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail

from .models import UserProfile

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def signup(request):
    return render(request, 'sign_up.html')

def enroll(request):
    return render(request, 'full_stack_enroll.html')

def course(request):
    return render(request, 'course.html')

from django.core.mail import send_mail
from django.http import HttpResponse

def send_otp(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request"
        })

    data = json.loads(request.body)

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if password != confirm_password:
        return JsonResponse({
            "success": False,
            "error": "Passwords do not match"
        })

    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "success": False,
            "error": "Email already registered"
        })

    if UserProfile.objects.filter(phone=phone).exists():
        return JsonResponse({
            "success": False,
            "error": "Phone number already registered"
        })

    otp = str(random.randint(100000, 999999))

    request.session["otp"] = otp
    request.session["otp_time"] = int(time.time())

    request.session["full_name"] = full_name
    request.session["email"] = email
    request.session["phone"] = phone
    request.session["password"] = password

    send_mail(
        "Futuro Focus OTP Verification",
        f"Your OTP is {otp}. It is valid for 2 minutes.",
        "nitinsumna@gmail.com",
        [email],
        fail_silently=False,
    )

    return JsonResponse({
        "success": True
    })

def verify_otp(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request"
        })

    data = json.loads(request.body)

    entered_otp = data.get("otp")

    stored_otp = request.session.get("otp")
    otp_time = request.session.get("otp_time")

    if not stored_otp:
        return JsonResponse({
            "success": False,
            "error": "OTP not found"
        })

    if int(time.time()) - otp_time > 120:
        return JsonResponse({
            "success": False,
            "error": "OTP expired"
        })

    if entered_otp != stored_otp:
        return JsonResponse({
            "success": False,
            "error": "Incorrect OTP"
        })

    full_name = request.session.get("full_name")
    email = request.session.get("email")
    phone = request.session.get("phone")
    password = request.session.get("password")

    username = email

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=full_name
    )

    UserProfile.objects.create(
        user=user,
        phone=phone
    )
    # Automatically log in user
    login(request, user)

    
    # Clear session data
    request.session.pop("otp", None)
    request.session.pop("otp_time", None)
    request.session.pop("full_name", None)
    request.session.pop("email", None)
    request.session.pop("phone", None)
    request.session.pop("password", None)

    return JsonResponse({
        "success": True,
        "redirect": "/home/"
    })

def resend_otp(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request"
        })

    email = request.session.get("email")

    if not email:
        return JsonResponse({
            "success": False,
            "error": "Session expired"
        })

    otp = str(random.randint(100000, 999999))

    request.session["otp"] = otp
    request.session["otp_time"] = int(time.time())

    send_mail(
        "Futuro Focus OTP Verification",
        f"Your new OTP is {otp}. It is valid for 2 minutes.",
        "nitinsumna@gmail.com",
        [email],
        fail_silently=False,
    )

    return JsonResponse({
        "success": True
    })

def login_user(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Invalid request"
        })

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    user = authenticate(
        request,
        username=email,
        password=password
    )

    if user is None:
        return JsonResponse({
            "success": False,
            "error": "Invalid email or password"
        })

    login(request, user)

    return JsonResponse({
        "success": True,
        "redirect": "/home/"
    })

def logout_user(request):
    logout(request)
    return redirect('signup')