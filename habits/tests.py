from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(
            email="testov@test.ru", password="123abc", tg_id="12345"
        )
        self.client.force_authenticate(user=self.user)
        """Создание тестовой привычки"""
        self.habit = Habit.objects.create(
            place="place_test",
            time="2024-07-22 16-00",
            owner=self.user,
            action="бегать",
            is_pleasant=False,
            periodicity=1,
            period_time=60,
            reward="съесть конфету",
            is_public=True,
            related_habit=None,
        )

    def test_habit_create(self):
        """Тестирование создания привычки"""
        url = reverse("habits:habits-create")
        data = {
            "place": "place_test1",
            "time": "2024-05-27 08:40",
            "owner": self.user.pk,
            "action": "купаться",
            "periodicity": 2,
            "period_time": 119,
            "reward": "съесть торт",
            "is_public": True,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Тестирование обновления привычки"""
        url = reverse("habits:habits-update", args=(self.habit.pk,))
        data = {"place": "place_update", "action": "плавать"}
        response = self.client.patch(url, data)
        data1 = response.json()
        print(data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(data.get("place"), "place_update")

    def test_habit_retrieve(self):
        """Тестирование просмотра информации о привычке"""
        url = reverse("habits:habits-retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_delete(self):
        """Тестирование удаления урока"""
        url = reverse("habits:delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        print(f"{self.habit.action} удалён")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

        # self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_habit_list(self):
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        data = response.json
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_period_time(self):
        """Тестирование времени на выполнение привычки."""
        url = reverse("habits:habits-create")
        data = {
            "owner": self.user.pk,
            "place": "Место тест",
            "time": "2024-05-27 08:40",
            "action": "Чистить зубы",
            "period_time": "121",
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_periodicity(self):
        """Тестирование периодичности привычки."""
        url = reverse("habits:habits-create")
        data = {
            "owner": self.user.pk,
            "place": "Место тест",
            "action": "Умываться",
            "time": "2024-05-27 08:40",
            "periodicity": 8,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_habit_list(self):
        """Тестирование списка привычек конкретного пользователя"""
        response = self.client.get(reverse("habits:user-habits"))
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "place": "place_test",
                    "time": "2024-07-22T16:00:00Z",
                    "action": "бегать",
                    "is_pleasant": False,
                    "periodicity": 1,
                    "reward": "съесть конфету",
                    "period_time": 60,
                    "is_public": True,
                    "owner": self.user.pk,
                    "related_habit": None,  # self.habit.related_habit
                }
            ],
        }
        self.assertEqual(data, result)
