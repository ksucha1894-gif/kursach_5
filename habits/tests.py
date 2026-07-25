from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit


class HabitTestCase(APITestCase):
    """Комплексное тестирование бэкенд-логики приложения Habits."""

    def setUp(self):
        """Первоначальная настройка перед запуском каждого теста."""
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email="test@yandex.ru", password="testpassword123", username="testuser"
        )
        # Авторизуем пользователя в клиенте API
        self.client.force_authenticate(user=self.user)

        # Создаем базовую приятную привычку для тестов
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            action="Выпить стакан воды",
            time="08:00:00",
            place="Кухня",
            is_pleasant=True,
            duration=30,
            periodicity=1,
        )

    def test_create_habit(self):
        """Тестирование успешного создания привычки."""
        url = reverse("habits:habit-create")
        data = {
            "action": "Сделать зарядку",
            "time": "08:30:00",
            "place": "Гостиная",
            "duration": 60,
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(action="Сделать зарядку").count(), 1)

    def test_habit_duration_validator(self):
        """Тестирование валидатора ограничения времени (не более 120 секунд)."""
        url = reverse("habits:habit-create")
        data = {
            "action": "Долгий бег",
            "time": "07:00:00",
            "place": "Парк",
            "duration": 200,  # Ошибка! Нарушение больше 120
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_habit_list(self):
        """Тестирование успешного получения списка привычек пользователя."""
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        """Тестирование редактирования привычки владельцем."""
        url = reverse("habits:habit-update", kwargs={"pk": self.pleasant_habit.pk})
        data = {"action": "Выпить два стакана воды"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pleasant_habit.refresh_from_db()
        self.assertEqual(self.pleasant_habit.action, "Выпить два стакана воды")

    def test_delete_habit(self):
        """Тестирование удаления привычки владельцем."""
        url = reverse("habits:habit-delete", kwargs={"pk": self.pleasant_habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
