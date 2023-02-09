from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps import utils
from apps.users.services import UserService

User = get_user_model()


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
        if not UserService.exists(attrs):
            raise serializers.ValidationError({"email": "User with email: {} doesn't exists".format(attrs["email"])})
        return attrs


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Password-Reset-Confirm-Serializer"""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "invalid_token": _("Invalid token for given user."),
        "invalid_uid": _("Invalid user id or user doesn't exist."),
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = UserService.get({"pk": uid})
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError({"uid": [self.error_messages[key_error]]}, code=key_error)

        try:
            validate_password(attrs["new_password"], self.user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        is_token_valid = default_token_generator.check_token(self.user, self.initial_data.get("token", ""))
        if is_token_valid:
            validated_data.update({"user": self.user})
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError({"token": [self.error_messages[key_error]]}, code=key_error)


class ChangePasswordSerializer(serializers.Serializer):
    """ChangePasswordSerializer"""
    new_password = serializers.CharField()
    def validate(self, attrs: Dict[str, Any]):
        try:
            print(90, attrs)
            validate_password(attrs["new_password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return attrs
