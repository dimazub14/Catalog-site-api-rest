from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.users.api.serializers import UserRegistrationSerializer
from apps.users.models import User
from apps.users.services import UserService

class RegistrationUserAPIView(GenericAPIView):
    """Registration User"""
    service_class = UserService
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service_class.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
