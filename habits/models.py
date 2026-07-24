import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """
    Модель, представляющая привычку пользователя.

    Содержит настройки периодичности, длительности, места и времени выполнения,
    а также механизмы вознаграждения за полезные действия.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")

    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")

    associated_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная приятная привычка",
    )

    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )

    duration = models.PositiveIntegerField(
        default=60, verbose_name="Длительность (в секундах)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    def clean(self):
        """Валидация бизнес-логики привычек."""
        super().clean()

        if self.reward and self.associated_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if self.duration > 120:
            raise ValidationError(
                "Длительность выполнения привычки не должна превышать 120 секунд."
            )

        if self.associated_habit and not self.associated_habit.is_pleasant:
            raise ValidationError(
                "В связанные привычки можно добавлять только приятные привычки."
            )

        if self.is_pleasant:
            if self.reward or self.associated_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        if self.periodicity > 7:
            raise ValidationError(
                "Периодичность не может быть реже, чем один раз в 7 дней."
            )

    def save(self, *args, **kwargs):
        """Автоматический запуск полной валидации перед сохранением в БД."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        """Возвращает строковое представление привычки."""
        return f"{self.action} в {self.time} ({self.place})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
