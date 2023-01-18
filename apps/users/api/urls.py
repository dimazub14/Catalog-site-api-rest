from django.urls import path

from apps.users.api import views

app_name = "users_app"

urlpatterns = [
    path("registration/", views.RegistrationUserAPIView.as_view(), name="registration"),
]
