from datetime import timedelta

from rest_framework.serializers import ValidationError

from habits.models import Habit


class RelatedHabitOrRewardValidator:
    """Проверка заполнения полей связанной привычки и вознаграждения: должно быть заполнено только одно поле"""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)   #value.get('related_habit')
        reward = dict(value).get(self.field2)
        if related_habit and reward:
            raise ValidationError('Два поля связанной привычки и вознаграждения не могут быть заполнены вместе, '
                                  'выберите что-то одно')


class PleasantHabitValidator:
    """Проверка на отсутствие у приятной привычки полей связанной привычки и вознаграждения"""

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)  # value.get('related_habit')
        reward = dict(value).get(self.field2)
        is_pleasant = dict(value).get(self.field3)
        if is_pleasant:
            if reward or related_habit:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')


class RelatedHabitValidator:
    """Проверка на принадлежность связанной привычки к приятным: связать с полезной привычкой
    можно только приятную привычку
    """

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        related_habit = dict(value).get(self.field1)  # value.get('related_habit')
        reward = dict(value).get(self.field2)
        is_pleasant = dict(value).get(self.field3)
        if related_habit and reward and is_pleasant:
            raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки.')


def duration_validator(duration):
    """Проверка продолжительности выполнения привычки:
     Должна быть не более 2 минут"""

    if duration > timedelta(minutes=2):
        raise ValidationError('Время выполнения должно быть не больше 120 секунд.')