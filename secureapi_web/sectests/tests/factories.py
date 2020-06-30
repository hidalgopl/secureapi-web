import secrets
import uuid

from factory import DjangoModelFactory

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.users.models import CLIToken, User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


class CLITokenFactory(DjangoModelFactory):
    class Meta:
        model = CLIToken


class SecTestSuiteFactory(DjangoModelFactory):
    class Meta:
        model = SecTestSuite
