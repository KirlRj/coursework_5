from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    place = models.CharField(max_length=200, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=500, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (дней)"
    )
    reward = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="Вознаграждение"
    )
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение (сек)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user} — {self.action} в {self.time}"
