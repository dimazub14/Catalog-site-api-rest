from django.urls import path
from apps.users.api import views


app_name = "users"

urlpatterns = [
    path('registration/', views.RegistrationUserAPIView.as_view(), name="registration"),
]
