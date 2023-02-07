import unittest

from faker import Faker

from apps.users.api import serializers
from tests.factory import UserFactory
from tests.factory.users import EmailFactory

fake = Faker()


class TestSiteAdminRegisterSerializer(unittest.TestCase):
    """Class for test SiteAdminRegisterSerializer"""

    def setUp(self):
        # self.user = SiteAdminFactory()
        self.data = {"name": "test", "password": "TestTest123", "email": "test@gmail.com"}
        self.serializer = serializers.UserRegistrationSerializer
        self.email = {"email": "somesomegmail.com"}

    def test_serializer_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertListEqual(
            list(serializer.errors.keys()),
            ["name", "email", "password"],
        )

    def test_serializer_exist_email(self):
        """Test serializer exists email"""
        user = UserFactory()
        data = {"email": user.email, "name": "Test", "password": "TestTest123"}
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertListEqual(list(serializer.errors.keys()), ["email"])

    def test_serializer_validate_password(self):
        """Test serializer validate_password"""
        data = {"email": "johnsmith@gmail.com", "name": "Test", "password": "123"}
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertListEqual(list(serializer.errors.keys()), ["password"])

    def test_serializer_validate(self):
        """Test serializer validated data"""
        serializer = self.serializer(data=self.data)
        self.assertTrue(serializer.is_valid())


class TestResetPasswordSerializer(unittest.TestCase):
    """Test-Reset-Password-Serializer"""

    def setUp(self) -> None:
        self.user = EmailFactory()
        self.data = {"email": self.user.email}
        self.serializer = serializers.ResetPasswordSerializer
        self.wrong_email = {"email": "somesome@gmail.com"}

    def test_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data=self.data)
        serializer.is_valid()
        self.assertEqual(list(serializer.data.keys()), ["email"])

    def test_wrong_email(self):
        serializer = self.serializer(data=self.wrong_email)
        self.assertFalse(serializer.is_valid())

    def test_no_email(self):
        serializer = self.serializer(data={})
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())

    # TODO: Case 1 - wrong email format. somesome@gmail.com
    # TODO: Case 2 - Email not found.


class TestPasswordResetConfirmSerializer(unittest.TestCase):
    """Test-Password-Reset-Confirm-Serializer"""

    def setUp(self) -> None:
        self.data = {"uid": "Invalid uid", "new_password": "Invalid new_password", "token": "Invalid token"}
        self.serializer = serializers.PasswordResetConfirmSerializer

    def test_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data=self.data, many=False)
        serializer.is_valid()
        self.assertEqual(list(serializer.data.keys()), ["uid", "token", "new_password"])

    # def validate_new_password(self, value):
    #     user = getattr(self, "user", None) or self.context["request"].user

    # TODO: Case - 1 Invalid uid
    # TODO: Case - 2 Invalid token
