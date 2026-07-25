from rest_framework import serializers

from .models import Habit
from .validators import (AssociatedHabitIsPleasantValidator, DurationValidator,
                         PeriodicityValidator,
                         PleasantHabitRestrictionsValidator,
                         RewardAndAssociatedHabitValidator)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели привычки с полной валидацией API."""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardAndAssociatedHabitValidator(
                reward_field="reward",
                associated_habit_field="associated_habit",
            ),
            DurationValidator(duration_field="duration"),
            AssociatedHabitIsPleasantValidator(
                associated_habit_field="associated_habit"
            ),
            PleasantHabitRestrictionsValidator(
                is_pleasant_field="is_pleasant",
                reward_field="reward",
                associated_habit_field="associated_habit",
            ),
            PeriodicityValidator(periodicity_field="periodicity"),
        ]
