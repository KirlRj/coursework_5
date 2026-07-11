from rest_framework import serializers

from .models import Habit
from .validators import (validate_duration, validate_periodicity,
                         validate_pleasant_habit_no_reward,
                         validate_related_habit_is_pleasant,
                         validate_reward_and_related_habit)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        validate_reward_and_related_habit(data)
        validate_duration(data)
        validate_related_habit_is_pleasant(data)
        validate_pleasant_habit_no_reward(data)
        validate_periodicity(data)
        return data
