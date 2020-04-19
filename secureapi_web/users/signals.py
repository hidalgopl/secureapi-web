import slack
from django.conf import settings
from django.dispatch import receiver
from djoser.compat import get_user_email
from djoser.signals import user_activated
from templated_mail.mail import BaseEmailMessage

from secureapi_web.users.models import CLIToken


class WelcomeEmail(BaseEmailMessage):
    template_name = "email/confirmation.html"


@receiver(user_activated)
def send_welcoming_email(sender, user, request, *args, **kwargs):
    context = {"user": user, "slack_invitation_url": settings.SLACK_INVITE_URL}
    to = [get_user_email(user)]
    WelcomeEmail(request, context).send(to)


@receiver(user_activated)
def create_cli_token(sender, user, request, *args, **kwargs):
    CLIToken.objects.create(user=user)


@receiver(user_activated)
def notify_on_slack(sender, user, request, *args, **kwargs):
    if settings.SLACK_NOTIFY_ENABLED:
        msg = f"User with email: {user.email} logged in for first time. Invite him on slack!"
        client = slack.WebClient(
            token=settings.SLACK_TOKEN
        )
        resp = client.chat_postMessage(
            channel=settings.SLACK_NOTIFY_CHANNEL,
            text=msg
        )
        assert resp["ok"]
