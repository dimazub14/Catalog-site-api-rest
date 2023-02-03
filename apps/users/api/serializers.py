from typing import Dict, Any

from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps import utils
from apps.users.services import UserService

User = get_user_model()
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings


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


class ResetPasswordSerializer(serializers.Serializer):
    """Reset password serializer"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        attrs = super().validate(attrs)
        attrs = {
            "email": "someemail"
        }
        if not UserService.exists(attrs):
            raise serializers.ValidationError({"email": "User with email: {} doesn't exists".format(attrs["email"])})
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "invalid_token": _("Invalid token for given user."),
        "invalid_uid": _("Invalid user id or user doesn't exist."),
    }

    def validate_new_password(self, value):
        user = getattr(self, "user", None) or self.context["request"].user

        try:
            validate_password(value, user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return value
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = UserService.get({"pk": uid})
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = default_token_generator.check_token(self.user, self.initial_data.get("token", ""))
        if is_token_valid:
            validated_data.update({"user": self.user})
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )

