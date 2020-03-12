import slack
from django.conf import settings


def notify_on_slack(backend, details, user=None, *args, **kwargs):
    email = details.get("email")
    if email:
        msg = f"User with email: {email} logged in for first time. Invite him on slack!"
        client = slack.WebClient(
            token=settings.SLACK_TOKEN
        )
        resp = client.chat_postMessage(
            channel=settings.SLACK_NOTFIY_CHANNEL,
            text=msg
        )
        assert resp["ok"]


