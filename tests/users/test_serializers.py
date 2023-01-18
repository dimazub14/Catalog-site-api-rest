import unittest

from apps.users.api import serializers
from tests.factory import UserFactory


class TestSiteAdminRegisterSerializer(unittest.TestCase):
    """Class for test SiteAdminRegisterSerializer"""

    def setUp(self):
        # self.user = SiteAdminFactory()
        self.data = {"name": "test", "password": "TestTest123", "email": "test@gmail.com"}
        self.serializer = serializers.UserRegistrationSerializer

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
