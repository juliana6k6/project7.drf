from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RelatedHabitOrRewardValidator, PleasantHabitValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitOrRewardValidator(field1="related_habit", field2="reward"),
            NotPleasantHabitValidator(field1="related_habit", field2="reward", field3="is_pleasant"),

