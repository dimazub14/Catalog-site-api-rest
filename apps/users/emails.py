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
        print("Pk", user.pk)
        encode = utils.encode_uid(user.pk)
        print("Encode Pk", encode)
        print("Decode PK", utils.decode_uid(encode))
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        print(19, context["uid"])
        print(20, context["token"])
        print(21, context["url"])
        return context
