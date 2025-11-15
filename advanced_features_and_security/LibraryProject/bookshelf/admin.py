from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Author, Book, CustomUser, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('title', 'author', 'publication_year')

    # Filters to allow quick sorting and categorization
    list_filter = ('publication_year', 'author')

    # Search capability by title and author
    search_fields = ('title', 'author')

#registering the new CustomUserModel
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Specify the model
    model = CustomUser

    # Add custom fields to the user detail view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    # Columns to display in the user list view
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']

# Register the CustomUser model with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)