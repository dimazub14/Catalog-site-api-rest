from django.urls import path

from apps.users.api import views

app_name = "users_app"

urlpatterns = [
    path("registration/", views.RegistrationUserAPIView.as_view(), name="registration"),
    path("token/", views.LoginAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", views.RefreshAPIView.as_view(), name="token_refresh"),
    path("reset-password/", views.ResetPasswordAPIView.as_view(), name="reset_password"),
    path("reset-password-confirm/", views.ResetPasswordConfirmAPIView.as_view(), name="reset_password_confirm"),
    path("change-password/", views.ChangePasswordAPIView.as_view(), name="change_password"),
]
