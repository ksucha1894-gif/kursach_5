from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Настройка отображения модели привычек в Django-админке."""

    list_display = ("id", "user", "action", "time", "place", "is_pleasant")
    list_filter = ("is_pleasant", "is_public", "user")
    search_fields = ("action", "place")

    def save_model(self, request, obj, form, change):
        """Автоматически привязывает текущего залогиненного пользователя к привычке."""
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)
