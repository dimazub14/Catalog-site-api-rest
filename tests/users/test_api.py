from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from faker import Faker

from tests.factory import UserFactory
fake = Faker()

class TestRegistrationAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("api:users_app:registration")
        self.data = {"name": "test", "password": "TestTest123", "email": "test@gmail.com"}

    def test_url(self):
        url = "/api/v1/users/registration/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestLoginAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("api:users_app:token_obtain_pair")
        password = "TestTest123"
        self.user = UserFactory(password=make_password(password))
        self.data = {
            "email": self.user.email,
            "password": password
        }

    def test_url(self):
        url = "/api/v1/users/login/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        data = self.data.copy()
        data["password"] = "Wrong Password"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        data = self.data.copy()
        data["email"] = fake.email()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")







