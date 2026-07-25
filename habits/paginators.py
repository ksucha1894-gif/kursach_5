from rest_framework.pagination import LimitOffsetPagination


class HabitPaginator(LimitOffsetPagination):
    """Кастомная пагинация для списка привычек."""

    default_limit = 5
    max_limit = 10
