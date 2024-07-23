from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


# Create your tests here.
class UsersTestCase(APITestCase):
    """Тестирование пользователей"""
    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@sky.pro")
        self.user.set_password("12345")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тестирование создания пользователя"""
        url = reverse("users:user_register")
        data = {
            "email": "user1@mail.ru",
            "password": "abcde"
        }
        response = self.client.post(url, data=data)
        print("\Пользователь создан.")
        print(response.json())
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
