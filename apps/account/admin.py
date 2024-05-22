from django.contrib import admin
from .models import CustomUser

# Register your models here.


class UserPanel(admin.ModelAdmin):
    search_fields = ["email"]


admin.site.register(CustomUser, UserPanel)