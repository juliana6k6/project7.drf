from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


# class HabitViewSet(ModelViewSet):
#     queryset = Habit.objects.all()
#     serializer_class = HabitSerializer


class HabitsCreateAPIView(CreateAPIView):
    """Эндпоинт создания привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitsRetrieveAPIView(RetrieveAPIView):
    """Эндпоинт отображения одной привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsUpdateAPIView(UpdateAPIView):
    """Эндпоинт редактирования привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsDestroyAPIView(DestroyAPIView):
    """Эндпоинт удаления привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitsListAPIView(ListAPIView):
    """Эндпоинт вывода списка привычек c признаком публичности"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPaginator


    def get_queryset(self):
        """Фильтруем список привычек по признаку публикации"""
        return Habit.objects.filter(is_published=True)


class UserHabitsListAPIView(ListAPIView):
    """Эндпоинт вывода списка привычек конкретного пользователя"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Фильтруем список привычек по текущему пользователю"""
        user = self.request.user
        queryset = Habit.objects.filter(owner=user)
        return queryset
