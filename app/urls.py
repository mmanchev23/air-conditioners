"""conditioners URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
    path("sign-up/", sign_up, name="sign_up"),
    path("sign-up/submit/", sign_up_submit, name="sign_up_submit"),
    path("sign-in/", sign_in, name="sign_in"),
    path("sign-in/submit/", sign_in_submit, name="sign_in_submit"),
    path("sigh-out/", sign_out, name="sign_out"),
    path("profile/<str:username>/", profile, name="profile"),
    path("profile/<str:username>/settings/", profile_edit, name="profile_edit"),
    path("profile/<str:username>/settings/submit/", profile_edit_submit, name="profile_edit_submit"),
    path("profile/<str:username>/delete/", profile_delete, name="profile_delete"),
    path("profile/<str:username>/delete/submit/", profile_delete_submit, name="profile_delete_submit"),
    path("applications/", applications, name="applications"),
    path("application/create/", application_create, name="application_create"),
    path("application/<uuid:id>/create/", application_create, name="application_create"),
    path("application/<uuid:id>/edit/", application_edit, name="application_edit"),
    path("application/<uuid:id>/delete/", application_delete, name="application_delete"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
