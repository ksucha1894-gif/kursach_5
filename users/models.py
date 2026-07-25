from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя для проекта Атомные привычки."""

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Номер телефона"
    )
    city = models.CharField(max_length=150, blank=True, null=True, verbose_name="Город")
    telegram_chat_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Telegram Chat ID"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
