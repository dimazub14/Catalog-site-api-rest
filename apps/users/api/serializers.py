from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""

    class Meta:
        """Meta class"""

        model = User
        fields = [
            "name",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_password(value: str) -> str:
        """Validate password"""
        validate_password(password=value)
        return value
