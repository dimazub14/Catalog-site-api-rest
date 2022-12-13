from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
