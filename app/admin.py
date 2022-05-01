from .models import *
from django.contrib import admin

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["title", "customer"]

admin.site.register(User)
admin.site.register(Application, ApplicationAdmin)
