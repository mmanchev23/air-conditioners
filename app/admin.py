from .models import *
from django.contrib import admin

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["title", "technician"]


admin.site.register(Administrator)
admin.site.register(Tech)
admin.site.register(Customer)
admin.site.register(Application, ApplicationAdmin)
