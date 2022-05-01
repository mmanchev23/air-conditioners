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
                password=password
            )
            
            user.save()
            login(request, user)
            messages.success(request, "You have signed up successfully!")
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

@login_required(redirect_field_name="sign_in/")
def profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None

    context = {
        "user": user,
    }

    return render(request, "app/profile.html", context)

@login_required(redirect_field_name="sign_in/")
def profile_edit(request, username):
    user = User.objects.get(pk=request.user.pk) or None

    context = {
        "user": user,
        "join_date": user.date_joined.date(),
    }

    return render(request, "app/profile_edit.html", context)

@login_required(redirect_field_name="sign_in/")
def profile_edit_submit(request, username):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk) or None

        # Profile Credentials
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if "img" in request.FILES:
            profile_picture = request.FILES["img"]
        else:
            profile_picture = user.profile_picture

        # Password Credentials
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        
        user.profile_picture = profile_picture

        context = {
            "user": user,
        }

        if current_password:
            if new_password:
                if confirm_password:
                    if user.check_password(current_password):
                        if new_password == confirm_password:
                            user.set_password(new_password)
                            user.save()
                            messages.success(request, "Password updated successfully!")
                            return HttpResponseRedirect(reverse("profile", kwargs=context))
                        else:
                            messages.error(request, "Passwords should match!")
                            return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
                    else:
                        messages.error(request, "That's not your current password!")
                        return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
                else:
                    messages.error(request, "'Confirm Password' field can not be empty!")
                    return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
            else:
                messages.error(request, "'New Password' field can not be empty!")
                return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
        else:
            pass

        user.save()

        messages.success(request, "Changes saved successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "An error occured!")
        return HttpResponseRedirect(reverse("index"))

@login_required(redirect_field_name="sign_in/")
def profile_delete(request, username):
    return render(request, "app/profile_delete.html")

@login_required(redirect_field_name="sign_in/")
def profile_delete_submit(request, username):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk) or None

        password = request.POST.get("password")

        context = {
            "user": user,
        }

        if user.check_password(password):
            user.delete()
            messages.success(request, "Profile deleted successfully!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Wrong password!")
            return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
    else:
        messages.error(request, "An error occured!")
        return HttpResponseRedirect(reverse("profile_edit", kwargs=context))

@login_required(redirect_field_name="sign_in/")
def applications(request):
    applications = Application.objects.all()
    users = User.objects.all()

    applications_paginator = Paginator(applications, 5)

    page_number = request.GET.get("page")

    try:
        application_obj = applications_paginator.get_page(page_number)
    except PageNotAnInteger:
        application_obj = applications_paginator.page(1)
    except EmptyPage:
        application_obj = applications_paginator.page(applications_paginator.num_pages)

    context = {
        "applications": application_obj,
        "users": users,
    }

    return render(request, "app/applications.html", context)

@login_required(redirect_field_name="sign_in/")
def application_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        address = request.POST.get("address")
        status = request.POST.get("status")
        date_of_visit_by_technician = request.POST.get("date_of_visit_by_technician")
        technician_id = request.POST.get("technician")

        technician = User.objects.get(pk=technician_id) or None
        
        if "img" in request.FILES:
            picture = request.FILES.get("img")
        else:
            picture = "../static/images/application.png"

        application = Application.objects.create(
            customer=request.user,
            title=title,
            description=description,
            address=address,
            status=status,
            date_of_visit_by_technician=date_of_visit_by_technician,
            technician=technician,
            image=picture
        )

        application.save()
        messages.success(request, f"Application created successfully!")
        return HttpResponseRedirect(reverse("applications"))
    else:
        return render(request, "app/applications.html")

@login_required(redirect_field_name="sign_in/")
def application_edit(request, id):
    if request.method == "POST":
        application = application.objects.get(pk=id) or None
        
        title = request.POST.get("title")
        description = request.POST.get("description")
        address = request.POST.get("address")
        status = request.POST.get("status")
        date_of_visit_by_technician = request.POST.get("date_of_visit_by_technician")
        technician = request.POST.get("technician")
        
        if "img" in request.FILES:
            picture = request.FILES.get("img")
        else:
            picture = "../static/images/application.png"

        application.title=title,
        application.description=description,
        application.address=address,
        application.status=status,
        application.date_of_visit_by_technician=date_of_visit_by_technician,
        application.technician=technician,
        application.picture=picture

        application.save()

        messages.success(request, f"Application updated successfully!")
        return HttpResponseRedirect(reverse("applications"))
    else:
        return render(request, "app/applications.html")

@login_required(redirect_field_name="sign_in/")
def application_delete(request, id):
    if request.method == "POST":
        application = application.objects.get(pk=id) or None
        application.delete()
        messages.success(request, f"Application deleted successfully!")
        return HttpResponseRedirect(reverse("applications"))
    else:
        return render(request, "app/applications.html")
