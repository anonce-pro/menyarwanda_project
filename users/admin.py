from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add any additional fields to display in the admin interface if needed
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "is_subscriber"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_subscriber",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("is_subscriber",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

