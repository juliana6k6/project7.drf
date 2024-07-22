from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(email="testov@test.ru", password="123abc", tg_id="12345")
        self.client.force_authenticate(user=self.user)
        """Создание тестовой привычки"""
        self.habit = Habit.objects.create(
            place="place_test", time="2024-07-22 16-00", owner=self.user, action="бегать",
            is_pleasant=False, periodicity=1, period_time=120,
            reward="съесть конфету", is_public=True, related_habit=None)


    def test_habit_create(self):
        """Тестирование создания привычки"""
        url = reverse("habits:habits-create")
        data = {"place": "place_test1", "time": "2024-05-27 08:40", "owner": self.user.id,
                "action": "купаться",
                "is_pleasant": False, "periodicity": 2, "period_time": 120, "reward": "съесть торт",
                "is_public": True}
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Lesson.objects.all().count(), 2)
        # self.assertEqual(
        #     response.json(),
        #     {
        #         "id": 2,
        #         "url": "https://course1.youtube.com/",
        #         "title": "Lesson1",
        #         "description": "Description_test",
        #         "preview": None,
        #         "course": 1,
        #         "owner": 1,
        #     },
        # )


    def test_habit_retrieve(self):
        """Тестирование просмотра информации о привычке"""
        url = reverse("habits:habits-retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)
#     def test_lesson_update(self):
#         """Тестирование редактирования урока"""
#         url = reverse("materials:lesson-update", args=(self.lesson.pk,))
#         data = {"title": "Lesson1_update", "description": "Description_update"}
#         response = self.client.patch(url, data)
#         data1 = response.json
#         print(data1)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.lesson.refresh_from_db()
#         self.assertEqual(data.get("title"), "Lesson1_update")
#
#     def test_lesson_delete(self):
#         """Тестирование удаления урока"""
#         url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
#         response = self.client.delete(url)
#         print(f"{self.lesson.title} удалён")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Lesson.objects.all().count(), 0)
#         self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
#
#         # self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
#
#     def test_lesson_list(self):
#         url = reverse("materials:lesson-list")
#         response = self.client.get(url)
#         data = response.json
#         print(data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Lesson.objects.all().count(), 1)
# from django.test import TestCase
#
# # Create your tests here.
