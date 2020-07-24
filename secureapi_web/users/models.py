import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .utils import cli_token_gen


class PaidTiers(models.IntegerChoices):
    FREE = 0
    FIRST_TIER = 50


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paid_tier = models.PositiveSmallIntegerField(choices=PaidTiers.choices, default=PaidTiers.FREE)

    @property
    def is_free(self):
        return self.paid_tier == PaidTiers.FREE


class CLIToken(models.Model):
    token = models.CharField(default=cli_token_gen, max_length=36)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.token[:3]}...{self.token[-3:]}"
