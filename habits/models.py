from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.models import User


class Habit(models.Model):
    """Модель привычки:
    Поле related_habit указывается только для полезной привычки
    Поле is_nice - признак приятной привычки, можно привязать к полезной
    Поле reward указывается только для полезной привычки, если нет привязки к приятной
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите владельца привычки",
        related_name="owner",
    )

    place = models.CharField(
        max_length=100, verbose_name="Место", help_text="Укажите где?"
    )
    time = models.DateTimeField(
        default=timezone.now().date(),
        verbose_name="Время в формате YYYY-MM-DD hh-mm",
        help_text="Укажите когда?",
    )
    action = models.CharField(
        max_length=100,
        verbose_name="Действие",
        help_text="Укажите совершаемое действие",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Можно привязать к полезной привычке",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="связанная приятная привычка",
        help_text="Указывается только для полезной привычки",
    )
    periodicity = models.PositiveIntegerField(
        verbose_name="Периодичность",
        default=7,
        help_text="Укажите периодичность выполнения привычки",
    )
    reward = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="вознаграждение",
        help_text="Указывается только для полезной привычки, если нет привязки к приятной",
    )
    period_time = models.PositiveIntegerField(
        default=120,
        verbose_name="время на выполнение в секундах",
        help_text="Укажите продолжительность выполнения",
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Признак публичности",
        help_text="Можно публиковать в общий доступ",
    )


    def __str__(self):
        return f"{self.action} в {self.time} {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("action",)
