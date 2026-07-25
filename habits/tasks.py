import datetime

import requests
from celery import shared_task
from django.conf import settings

from .models import Habit


@shared_task
def send_telegram_notifications():
    """Фоновая задача для проверки привычек и отправки напоминаний в Telegram."""
    now = datetime.datetime.now()
    current_time = now.time().replace(second=0, microsecond=0)

    # Фильтруем полезные привычки, у которых совпадает время выполнения
    habits = Habit.objects.filter(time=current_time, is_pleasant=False)

    for habit in habits:
        # Проверяем, что у пользователя заполнен чат-айди телеграма
        if (
            habit.user
            and hasattr(habit.user, "telegram_chat_id")
            and habit.user.telegram_chat_id
        ):
            chat_id = habit.user.telegram_chat_id
            message = (
                f"Привет! Время выполнять привычку: {habit.action} в {habit.place}."
            )

            # URL-запрос к серверам Telegram Bot API
            url = f"https://telegram.org{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": message}

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
            except requests.RequestException:
                pass
