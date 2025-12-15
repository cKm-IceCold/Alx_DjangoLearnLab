from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ( 'profile_photo', 'bio', 'followers')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)