import asyncio
import logging

import telegram
from celery import shared_task
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder():
    from .models import Habit

    now = timezone.localtime(timezone.now())
    current_time = now.time()
    logger.info(
        f"Запуск задачи. Текущее время: {current_time.hour}:{current_time.minute}"
    )

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
    ).select_related("user")

    logger.info(f"Найдено привычек: {habits.count()}")

    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

    for habit in habits:
        logger.info(
            f"Привычка: {habit.action}, время: {habit.time.hour}:{habit.time.minute}"
        )
        if (
            habit.time.hour == current_time.hour
            and habit.time.minute == current_time.minute
        ):
            message = (
                f"Напоминание о привычке!\n"
                f"Действие: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time}"
            )
            asyncio.run(
                bot.send_message(
                    chat_id=habit.user.telegram_chat_id,
                    text=message,
                )
            )
            logger.info(
                f"Сообщение отправлено пользователю {habit.user.telegram_chat_id}"
            )
