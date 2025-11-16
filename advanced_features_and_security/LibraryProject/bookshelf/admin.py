from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# --- Custom ModelAdmin (Step 4) ---

class CustomUserAdmin(UserAdmin):
    """
    Defines the admin interface for the CustomUser model.
    """
    # Overrides UserAdmin fields to work with CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    ordering = ('email',)

    # Configuration for the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ('Personal info', {
            'fields': (
                'first_name', 
                'last_name', 
                'date_of_birth', # Custom Field
                'profile_photo', # Custom Field
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Configuration for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'first_name',
                'last_name',
                'date_of_birth', # Custom Field
                'profile_photo', # Custom Field
                'password', 
                'password2', 
            )
        }),
    )

# Register the custom user model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)

# If you have other models in bookshelf/models.py (like Book, if you add it later), 
# you would register them below this line using:
# admin.site.register(Book)