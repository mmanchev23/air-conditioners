from .models import *
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    return render(request, "app/index.html")

def sign_up(request):
    return render(request, "app/sign_up.html")

def sign_up_submit(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        pin = request.POST.get("pin")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # First name validation
        if not first_name:
            messages.error(request, "The 'First name' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Last name validation
        if not last_name:
            messages.error(request, "The 'Last name' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Username validation
        if not username:
            messages.error(request, "The 'Username' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Email validation
        if not email:
            messages.error(request, "The 'Email' field can not be empty!")
            return render(request, "app/sign_up.html")

        # PIN validation
        if not pin:
            messages.error(request, "The 'PIN' field can not be empty!")
            return render(request, "app/sign_up.html")

        if len(pin) != 10:
            messages.error(request, "Your PIN should contain exactly 10 digits!")
            return render(request, "app/sign_up.html")

        # Phone number validation
        if not phone_number:
            messages.error(request, "The 'Phone number' field can not be empty!")
            return render(request, "app/sign_up.html")

        if len(phone_number) != 10:
            messages.error(request, "Your phone number should contain exactly 10 digits!")
            return render(request, "app/sign_up.html")

        # Password validation
        if not password:
            messages.error(request, "The 'Password' field can not be empty!")
            return render(request, "app/sign_up.html")

        if not confirm_password:
            messages.error(request, "The 'Confirm password' field can not be empty!")
            return render(request, "app/sign_up.html")

        has_atleast_eight_characters = False
        has_atleast_one_digit = any(map(str.isdigit, password))
        has_atleast_one_upper = any(map(str.isupper, password))
        has_atleast_one_lower = any(map(str.islower, password))
        has_no_forbidden = False

        if len(str(password)) >= 8:
            has_atleast_eight_characters = True

        if not str(password).__contains__('!') or not str(password).__contains__('$') or not str(password).__contains__('#') or not str(password).__contains__('%'):
            has_no_forbidden = True

        if password != confirm_password:
            messages.error(request, "Passwords must match!")
            return render(request, "app/sign_up.html")

        if not has_atleast_eight_characters:
            messages.error(request, "The password can not contain less than 8 characters!")
            return render(request, "app/sign_up.html", )

        if not has_atleast_one_digit:
            messages.error(request, "The password should contains atleast one digit!")
            return render(request, "app/sign_up.html")

        if not has_atleast_one_upper:
            messages.error(request, "The password should contains atleast one upper character!")
            return render(request, "app/sign_up.html")

        if not has_atleast_one_lower:
            messages.error(request, "The password should contains atleast one lower character!")
            return render(request, "app/sign_up.html")

        if not has_no_forbidden:
            messages.error(request, "The password should not contains '!', '$', '#' or '%'!")
            return render(request, "app/sign_up.html")

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                pin=pin,
                phone_number=phone_number,
                password=password
            )
            
            user.save()
            login(request, user)
            messages.success(request, "You have registered successfully!")
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            messages.error(request, "Username already taken!")
            return render(request, "app/sign_up.html")
    else:
        return render(request, "app/sign_up.html")

def sign_in(request):
    return render(request, "app/sign_in.html")

def sign_in_submit(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have signed in successfully!")
            return HttpResponseRedirect(reverse("index"))
        except:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "app/sign_in.html")
    else:
        return render(request, "app/sign_in.html")

@login_required(redirect_field_name="sign_in/")
def sign_out(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return HttpResponseRedirect(reverse("index"))
