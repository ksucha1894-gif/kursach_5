from rest_framework.serializers import ValidationError


class RewardAndAssociatedHabitValidator:
    """Запрет одновременного выбора вознаграждения и связанной привычки."""

    def __init__(self, reward_field, associated_habit_field):
        self.reward_field = reward_field
        self.associated_habit_field = associated_habit_field

    def __call__(self, value):
        reward = value.get(self.reward_field)
        associated_habit = value.get(self.associated_habit_field)
        if reward and associated_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )


class DurationValidator:
    """Ограничение длительности выполнения привычки (не более 120 секунд)."""

    def __init__(self, duration_field):
        self.duration_field = duration_field

    def __call__(self, value):
        duration = value.get(self.duration_field)
        if duration and duration > 120:
            raise ValidationError(
                "Длительность выполнения привычки не должна превышать 120 секунд."
            )


class AssociatedHabitIsPleasantValidator:
    """В связанные привычки могут попадать только приятные привычки."""

    def __init__(self, associated_habit_field):
        self.associated_habit_field = associated_habit_field

    def __call__(self, value):
        associated_habit = value.get(self.associated_habit_field)
        if associated_habit and not associated_habit.is_pleasant:
            raise ValidationError(
                "В связанные привычки можно добавлять только приятные привычки."
            )


class PleasantHabitRestrictionsValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""

    def __init__(self, is_pleasant_field, reward_field, associated_habit_field):
        self.is_pleasant_field = is_pleasant_field
        self.reward_field = reward_field
        self.associated_habit_field = associated_habit_field

    def __call__(self, value):
        is_pleasant = value.get(self.is_pleasant_field)
        reward = value.get(self.reward_field)
        associated_habit = value.get(self.associated_habit_field)
        if is_pleasant and (reward or associated_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class PeriodicityValidator:
    """Периодичность выполнения не может быть реже, чем 1 раз в 7 дней."""

    def __init__(self, periodicity_field):
        self.periodicity_field = periodicity_field

    def __call__(self, value):
        periodicity = value.get(self.periodicity_field)
        if periodicity and periodicity > 7:
            raise ValidationError(
                "Периодичность не может быть реже, чем один раз в 7 дней."
            )
