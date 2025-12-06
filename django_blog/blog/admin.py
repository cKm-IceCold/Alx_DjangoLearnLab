from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'location', 'updated_at')
    search_fields = ('user__username', 'location')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Profile Details', {'fields': ('bio', 'profile_picture', 'phone_number', 'location', 'website')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
