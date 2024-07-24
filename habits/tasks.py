from datetime import datetime

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_message_to_telegram


@shared_task
def send_message_about_habit():
    """Отправить напоминание о выполнение привычки"""
    current_datetime = timezone.now().today().replace(second=0, microsecond=0)
    #time_now = datetime.now().time().replace(second=0, microsecond=0)
    habits_list = Habit.objects.filter(is_nice=False)

    for habit in habits_list:
        chat_id = habit.owner.tg_id
        if habit.time >= time_now and chat_id is not None:
            message = f"Напоминание! Я буду {habit.action} в {habit.time_action} в {habit.place}."
            send_message_to_telegram(chat_id, message)