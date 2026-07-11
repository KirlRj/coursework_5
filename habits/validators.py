from rest_framework.serializers import ValidationError


def validate_reward_and_related_habit(data):
    if data.get("reward") and data.get("related_habit"):
        raise ValidationError(
            "Нельзя указывать одновременно вознаграждение и связанную привычку."
        )


def validate_duration(data):
    if data.get("duration") and data["duration"] > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_related_habit_is_pleasant(data):
    related = data.get("related_habit")
    if related and not related.is_pleasant:
        raise ValidationError(
            "В связанные привычки можно добавлять только приятные привычки."
        )


def validate_pleasant_habit_no_reward(data):
    if data.get("is_pleasant"):
        if data.get("reward") or data.get("related_habit"):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


def validate_periodicity(data):
    if data.get("periodicity") and data["periodicity"] > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")
