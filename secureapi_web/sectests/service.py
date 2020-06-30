from django.conf import settings

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.users.models import CLIToken
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions


class CLIAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_creds = request.META.get('HTTP_X_CLI_CREDS')
        username, access_key = auth_creds.split(":")
        if not username:
            raise exceptions.AuthenticationFailed('username or access_key is invalid')
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        if not CLIToken.objects.filter(user=user, token=access_key).exists():
            raise exceptions.AuthenticationFailed('username or access_key is invalid')
        return user, None


class CLIAuthService:
    def __init__(self, username, cli_token):
        self.username = username
        self.access_key = cli_token
        self.user_id = ""
        self.user_is_free = None

    def _fetch_from_db(self):
        # User = get_user_model()
        try:
            token = CLIToken.objects.select_related("user").get(token=self.access_key)
        except CLIToken.DoesNotExist:
            return None
        self.user_id = token.user.pk
        self.user_is_free = token.user.is_free
        return token

    def _validate_username(self, token):
        return self.username == token.user.username

    def has_valid_credentials(self):
        token = self._fetch_from_db()
        if token is None:
            return False
        return self._validate_username(token)

    def process_request(self):
        valid_credentials = True
        if not self.has_valid_credentials():
            valid_credentials = False
        exceeded_limit = self._has_exceeded_free_limit()
        valid = valid_credentials and not exceeded_limit
        return self.user_id, valid

    def _has_exceeded_free_limit(self):
        if not self.user_is_free:
            return False
        if settings.FREE_RUNS_LIMITED:
            return SecTestSuite.objects.filter(user_id=self.user_id).count() > settings.FREE_RUNS
        return False
