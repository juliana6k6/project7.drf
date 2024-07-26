import datetime
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


def create_message(habit):
    """Функция для создания сообщения"""
    if habit.reward:
        text_reward = f"После этого я могу {habit.reward}!"
    else:
        text_reward = f"После этого я могу {habit.related_habit.action}!"
    message = (
        f"Напоминание! Сегодня в {habit.time} в {habit.place} я буду {habit.action}"
        f"в течении {habit.period_time}! {text_reward}. Я  молодец!!!"
    )
    return message


@shared_task
def send_message_about_habit():
    """Функция проверяет все привычки. Отправляет напоминание о выполнение
    привычки в опреленное время и дату.
    После этого дата выполнения привычки меняется"""
    current_day = datetime.datetime.now().date()
    print(current_day)
    habits_list = Habit.objects.filter(is_pleasant=False, habit_date=current_day)
    print(habits_list)
    for habit in habits_list:
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
        chat_id = habit.owner.tg_id
        message = create_message(habit)
        if current_time == habit.time and chat_id is not None:
            send_telegram_message(chat_id, message)
            print("Сообщение отправляется")
            habit.habit_date = current_day + timedelta(days=habit.periodicity)
            habit.save()
