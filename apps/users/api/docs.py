from drf_spectacular.utils import OpenApiExample, inline_serializer
from rest_framework import serializers

from apps.users.api.serializers import ResetPasswordSerializer , PasswordResetConfirmSerializer
from apps.utils import SwaggerWrapper


class LoginSwagger(SwaggerWrapper):
    """Login-Documentation"""
    summary = "Login"
    description = "Endpoint for user registration. If successful, gives a pair of access/refresh tokens."
    User = ['Users']

    responses = {
        "200": inline_serializer(name="Response login", fields={"refresh":serializers.CharField(), "access":serializers.CharField()}),
    }
    request = inline_serializer(name="Request Login", fields={"email":serializers.EmailField(), "password":serializers.CharField()})

    examples=[
        OpenApiExample(
            name="login",
            value={
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NDA2MTg5NCwiaWF0IjoxNjc0MDUxMDk0LCJqdGkiOiIyODk4MzczYzE3OWY0Yjk5Yjg1NjVjYjBjODFlOGY4MSIsInVzZXJfaWQiOjF9.Yzq3XvmA7hceZtlKAEZSv3NJZ3MdOaNeqvedWWFOnJU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0MDU0Njk0LCJpYXQiOjE2NzQwNTEwOTQsImp0aSI6ImIwY2QzZWU5ZjAzNjRhNWZiYTAzMmUyOWNjYWFmYWE4IiwidXNlcl9pZCI6MX0.ZcKxkUJIdFTAsSLyW03l5KDC8B-6ldldSWUpGW436wY"
},
            summary="Example",
            description="Success example",
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Errors",
            value={
                "detail": [
                    "No active account found with the given credentials"
                ]
            },
            summary="Errors",
            description="Errors",
            response_only=True,
            status_codes=["401"]
        ),
        OpenApiExample(
            name="Errors",
            value={
                "email": [
                    "This field may not be blank."
                ],
                "password": [
                    "This field may not be blank."
                ]
            },
            summary="Errors",
            description="Errors",
            response_only=True,
            status_codes=["400"]
        ),
        OpenApiExample(
            name="Success",
            value={
                "email": "test@example.com",
                "password": "Example123"
            },
            summary="Success",
            description="Success",
            request_only=True,
            response_only=False,
        ),
    ]
class RefreshSwagger(SwaggerWrapper):
    """Refresh-Documentation"""
    summary = "refresh"
    description = "gives a pair of access/refresh tokens."
    User = ['Users']

    responses = {
        "200": inline_serializer(name="Response Refresh", fields={"access":serializers.CharField(), "refresh":serializers.CharField()}),
    }
    request = inline_serializer(name="Request Refresh", fields={"refresh":serializers.CharField()})

    examples=[
        OpenApiExample(
            name="refresh",
            value={
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NDA2MTg5NCwiaWF0IjoxNjc0MDUxMDk0LCJqdGkiOiIyODk4MzczYzE3OWY0Yjk5Yjg1NjVjYjBjODFlOGY4MSIsInVzZXJfaWQiOjF9.Yzq3XvmA7hceZtlKAEZSv3NJZ3MdOaNeqvedWWFOnJU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc0MDU0Njk0LCJpYXQiOjE2NzQwNTEwOTQsImp0aSI6ImIwY2QzZWU5ZjAzNjRhNWZiYTAzMmUyOWNjYWFmYWE4IiwidXNlcl9pZCI6MX0.ZcKxkUJIdFTAsSLyW03l5KDC8B-6ldldSWUpGW436wY"
},
            summary="Example",
            description="Refresh example",
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Success",
            value={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NDA2MTg5NCwiaWF0IjoxNjc0MDUxMDk0LCJqdGkiOiIyODk4MzczYzE3OWY0Yjk5Yjg1NjVjYjBjODFlOGY4MSIsInVzZXJfaWQiOjF9.Yzq3XvmA7hceZtlKAEZSv3NJZ3MdOaNeqvedWWFOnJU",
            },
            summary="Example",
            description="Refresh example",
            request_only=True,
            response_only=False
        ),
    ]

class ResetPasswordSwagger(SwaggerWrapper):
    """ResetPassword-Documentation"""
    summary = "ResetPassword"
    description = "Step 1. Enter the email that you received a confirmation email"
    User = ['Users']

    responses = {
        "204": None
    }
    request = ResetPasswordSerializer()

    examples=[
        OpenApiExample(
            name="Request Example",
            value={
                "email": "example@gmail.com"
            },
            summary="Example",
            description="Reset Password example",
            request_only=True
        ),
        OpenApiExample(
            name="Errors",
            value={
                "email": [
                        "User with email: not_exists@gmail.com doesn't exists"
                    ]
            },
            summary="Errors",
            description="Errors",
            response_only=True,
            status_codes=["400"]
        ),
    ]

class ResetPasswordConfirmSwagger(SwaggerWrapper):
    """ResetPasswordConfirm-Documentation"""
    summary = "ResetPasswordConfirm"
    description = "2.Step confirmation of password change."
    User = ['Users']

    responses = {
        "200": PasswordResetConfirmSerializer()
    }
    request = PasswordResetConfirmSerializer()

    examples=[
        OpenApiExample(
            name="ResetPasswordConfirm",
            value={
                "uid": "MzQ",
                "token": "bj06jz-44adc411781d4f8c41976dc5dde54c41",
                "new_password": "TestTest123"
},
            summary="Example",
            description="ResetPasswordConfirm example",
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            name="Errors",
            value={
                "uid": [
                   "Invalid user id or user doesn't exist."
                       ],
                "token": [
                    "Invalid token for given user."
                ]
            },
            summary="Errors",
            description="Errors",
            response_only=True,
            status_codes=["400"]
        ),
    ]

