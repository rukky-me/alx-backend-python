from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone_number", "role")


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")

    ordering = ("email",)
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number")}),
        ("Roles & Permissions", {
            "fields": ("role", "is_staff", "is_active", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )


admin.site.register(User, UserAdmin)
