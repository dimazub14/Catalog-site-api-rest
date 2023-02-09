import unittest

from faker import Faker

from apps.users.api import serializers
from tests.factory import UserFactory

fake = Faker()


class TestSiteAdminRegisterSerializer(unittest.TestCase):
    """Class for test SiteAdminRegisterSerializer"""

    def setUp(self):
        """setUp"""
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
        """setUp"""
        self.user = UserFactory()
        self.data = {"email": self.user.email}
        self.serializer = serializers.ResetPasswordSerializer
        self.wrong_email = {"email": "somesome@gmail.com"}

    def test_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data=self.data)
        serializer.is_valid()
        self.assertEqual(list(serializer.data.keys()), ["email"])

    def test_wrong_email(self):
        """test_wrong_email"""
        serializer = self.serializer(data=self.wrong_email)
        self.assertFalse(serializer.is_valid())

    def test_no_email(self):
        """test_no_email"""
        serializer = self.serializer(data={})
        serializer.is_valid()
        self.assertFalse(serializer.is_valid())


class TestPasswordResetConfirmSerializer(unittest.TestCase):
    """Test-Password-Reset-Confirm-Serializer"""

    def setUp(self) -> None:
        """setUp"""
        self.data = {"uid": "Invalid uid", "new_password": "Invalid new_password", "token": "Invalid token"}
        self.serializer = serializers.PasswordResetConfirmSerializer

    def test_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data=self.data, many=False)
        serializer.is_valid()
        self.assertEqual(list(serializer.data.keys()), ["uid", "token", "new_password"])


class TestChangePasswordSerializer(unittest.TestCase):
    """TestChangePasswordSerializer"""

    def setUp(self) -> None:
        """setUp"""
        self.data = {
            "new_password": "TestPassword123",
        }
        self.serializer = serializers.ChangePasswordSerializer

    def test_expected_fields(self):
        """Test serializer expected fields"""
        serializer = self.serializer(data={}, many=False)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(list(serializer.errors.keys()), ["new_password"])

    def test_not_valid_password(self):
        """Test serializer not valid password"""
        data = self.data.copy()
        data["new_password"] = "123"
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        print(115, serializer.errors)

class  TestPasswordSerializers(unittest.TestCase):
    """Test-Serializers-for-Password"""
    def setUp(self) -> None:
        """setUp"""
        self.data = {
            "new_password": "TestPassword123",
        }
        self.serializer = serializers.ChangePasswordSerializer

    def test_short_password(self):
        """Test serializer short_Password"""
        data = {
            "new_password": "TeXS2"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["new_password"][0], "This password is too short. It must contain at least 8 characters.")

    def test_numeric_password(self):
        """Test serializer numeric_Password"""
        data = {
            "new_password": "14725820593850684844848484848487474764646464646"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["new_password"][0],
                           "This password is entirely numeric.")

    def test_common_password(self):
        """Test serializer common_Password"""
        data = {
            "new_password": "password"
        }
        serializer = self.serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors["new_password"][0],
                          "This password is too common.")




