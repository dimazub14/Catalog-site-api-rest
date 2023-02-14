from django.utils.decorators import method_decorator
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api.docs import (
    ChangePasswordSwagger,
    LoginSwagger,
    RefreshSwagger,
    ResetPasswordConfirmSwagger,
    ResetPasswordSwagger,
)
from apps.users.api.serializers import (
    ChangePasswordSerializer,
    PasswordResetConfirmSerializer,
    ResetPasswordSerializer,
    UserRegistrationSerializer,
)
from apps.users.emails import PasswordResetEmail
from apps.users.services import UserService


class RegistrationUserAPIView(GenericAPIView):
    """Registration User"""

    service_class = UserService
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Registration method"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service_class.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(LoginSwagger.extend_schema, name="post")
class LoginAPIView(TokenObtainPairView):
    """Login APi View"""


@method_decorator(RefreshSwagger.extend_schema, name="post")
class RefreshAPIView(TokenRefreshView):
    """Refresh APi View"""


@method_decorator(ResetPasswordSwagger.extend_schema, name="post")
class ResetPasswordAPIView(GenericAPIView):
    """Reset-Password"""

    serializer_class = ResetPasswordSerializer
    service_class = UserService
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.service_class.get(serializer.validated_data)

        if user:
            context = {"user": user}
            to = [user.email]
            PasswordResetEmail(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(ResetPasswordConfirmSwagger.extend_schema, name="post")
class ResetPasswordConfirmAPIView(GenericAPIView):
    """Reset-Password-Confirm"""

    serializer_class = PasswordResetConfirmSerializer
    service_class = UserService
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service_class.change_password(
            user=serializer.validated_data["user"], password=serializer.validated_data["new_password"]
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(ChangePasswordSwagger.extend_schema, name="post")
class ChangePasswordAPIView(GenericAPIView):
    """ChangePassword"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    service_class = UserService

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service_class.change_password(user=request.user, password=serializer.validated_data["new_password"])
        return Response(status=status.HTTP_204_NO_CONTENT)
