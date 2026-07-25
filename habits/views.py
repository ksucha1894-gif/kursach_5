from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .paginators import HabitPaginator
from .permissions import IsOwner
from .serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания новой привычки."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Автоматически привязывает текущего пользователя к создаваемой привычке."""
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Возвращает привычки только того пользователя, который сделал запрос."""
        user = self.request.user
        if user.is_staff:
            return Habit.objects.all()
        return Habit.objects.filter(user=user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра одной конкретной привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для редактирования привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка всех публичных привычек (доступен всем)."""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = []  # Пустой список означает доступ без авторизации!
    pagination_class = HabitPaginator
