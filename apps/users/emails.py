from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from apps import utils


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):  # pylint: disable=W0221
        # PasswordResetEmail can be deleted
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJANGO_PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
