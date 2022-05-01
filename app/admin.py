from .models import *
from django.contrib import admin

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["title", "technician"]


admin.site.register(User)
admin.site.register(Application, ApplicationAdmin)
