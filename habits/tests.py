from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            duration=60,
            periodicity=1,
        )

    def test_habit_list(self):
        url = reverse("habits:habit_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create(self):
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бег",
            "duration": 90,
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Бег")

    def test_habit_retrieve(self):
        url = reverse("habits:habit_detail", args=[self.habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Зарядка")

    def test_habit_update(self):
        url = reverse("habits:habit_detail", args=[self.habit.pk])
        data = {
            "place": "Улица",
            "time": "08:00:00",
            "action": "Прогулка",
            "duration": 60,
            "periodicity": 1,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Прогулка")

    def test_habit_delete(self):
        url = reverse("habits:habit_detail", args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_public_habits_list(self):
        Habit.objects.create(
            user=self.user,
            place="Спортзал",
            time="10:00:00",
            action="Жим",
            duration=100,
            is_public=True,
        )
        url = reverse("habits:habit_public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data["count"], 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        url = reverse("habits:habit_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_cannot_access_habit(self):
        other_user = User.objects.create_user(username="other", password="otherpass")
        self.client.force_authenticate(user=other_user)
        url = reverse("habits:habit_detail", args=[self.habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_validator_reward_and_related_habit(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Кофе",
            duration=10,
            is_pleasant=True,
        )
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Читать",
            "duration": 60,
            "reward": "Шоколадка",
            "related_habit": pleasant.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_duration_max(self):
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Медитация",
            "duration": 121,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_related_habit_must_be_pleasant(self):
        non_pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Уборка",
            duration=60,
            is_pleasant=False,
        )
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Читать",
            "duration": 60,
            "related_habit": non_pleasant.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_pleasant_habit_no_reward(self):
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Кофе",
            "duration": 10,
            "is_pleasant": True,
            "reward": "Конфета",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_periodicity_max(self):
        url = reverse("habits:habit_list_create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Бег",
            "duration": 60,
            "periodicity": 8,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagination(self):
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                place="Дом",
                time="09:00:00",
                action=f"Привычка {i}",
                duration=60,
            )
        url = reverse("habits:habit_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]), 5)
