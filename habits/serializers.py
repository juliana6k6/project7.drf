from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from habits.validators import RelatedHabitOrRewardValidator, PleasantHabitValidator, RelatedHabitValidator


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RelatedHabitOrRewardValidator(field1="related_habit", field2="reward"),
            PleasantHabitValidator(field1="related_habit", field2="reward", field3="is_pleasant"),
            RelatedHabitValidator(field1="related_habit", field2="is_pleasant")


