from django.dispatch import receiver
from django.db.models.signals import post_delete
from allauth.account.signals import user_signed_up

from secureapi_web.users.models import CLIToken


@receiver(user_signed_up)
def create_cli_token(request, user, **kwargs):
    CLIToken.objects.create(
        user=user
    )


@receiver(post_delete, sender=CLIToken)
def recreate_new(sender, instance, **kwargs):
    CLIToken.objects.create(user=instance.user)
