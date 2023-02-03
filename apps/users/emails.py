from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from apps import utils


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()
        user = context.get("user")
        encode = utils.encode_uid(user.pk)
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
