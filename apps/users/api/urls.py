from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.api import views

app_name = "users_app"

urlpatterns = [
    path("registration/", views.RegistrationUserAPIView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
