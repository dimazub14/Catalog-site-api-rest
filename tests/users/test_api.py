from django.contrib.auth.hashers import make_password
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.api import views

from tests.factory import UserFactory

fake = Faker()


class TestRegistrationAPITestCase(APITestCase):
    """RegistrationAPITest"""

    def setUp(self) -> None:
        """setUp"""
        self.url = reverse("api:users_app:registration")
        self.data = {"name": "test", "password": "TestTest123", "email": "test@gmail.com"}

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/registration/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        """test_success_case"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLoginAPITestCase(APITestCase):
    """LoginTest"""

    def setUp(self) -> None:
        """setUp"""
        self.url = reverse("api:users_app:token_obtain_pair")
        password = "TestTest123"
        self.user = UserFactory(password=make_password(password))
        self.data = {"email": self.user.email, "password": password}

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/token/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        """test_success_case"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        """test_wrong_password"""
        data = self.data.copy()
        data["password"] = "Wrong Password"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        """test_not_found"""
        data = self.data.copy()
        data["email"] = fake.email()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "No active account found with the given credentials")


class TestRefreshAPITestCase(APITestCase):
    """RefreshTest"""

    def setUp(self) -> None:
        """setUp"""
        self.url = reverse("api:users_app:token_refresh")
        password = "TestTest123"
        self.user = UserFactory(password=make_password(password))
        self.data = {"email": self.user.email, "password": password}

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/token/refresh/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestResetPasswordAPIView(APITestCase):
    """ResetPassword"""

    def setUp(self) -> None:
        self.url = reverse("api:users_app:reset_password")
        self.data = {"email": "test@gmail.com"}

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/reset-password/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        """success_case"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestResetPasswordConfirmAPIView(APITestCase):
    """ResetPasswordConfirm"""

    def setUp(self) -> None:
        """setUp"""
        self.url = reverse("api:users_app:reset_password_confirm")
        self.data = {"uid": "MzQ", "new_password": "TestTest123", "token": "bj06jz-44adc411781d4f8c41976dc5dde54c41"}

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/reset-password-confirm/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_case(self):
        """test_success_case"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestChangePasswordAPIView(APITestCase):
    """ChangePassworAPIView"""
    def setUp(self) -> None:
        """setUp"""
        self.url = reverse("api:users_app:change_password")
        self.data = {"new_password": "TestTest123"}
        self.user = UserFactory()

    def test_url(self):
        """test_url"""
        url = "/api/v1/users/change-password/"
        self.assertEqual(url, self.url)
        response = self.client.post(self.url)
        self.assertNotIn(response.status_code, [status.HTTP_404_NOT_FOUND, status.HTTP_405_METHOD_NOT_ALLOWED])

    def test_empty_data_unauthorized(self):
        """test_empty_data"""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized(self):
        """test_success_case"""
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_changed(self):
        """force_authenticate"""
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
