from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения кастомной модели пользователей в Django-админке."""

    list_display = ("id", "username", "email", "phone", "city", "is_staff")
    search_fields = ("username", "email", "phone")
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "city", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "city", "avatar")}),
    )
