from secureapi_web.users.models import CLIToken


class CLIAuthService:
    def __init__(self, username, cli_token):
        self.username = username
        self.access_key = cli_token
        self.user_id = ""

    def _fetch_from_db(self):
        # User = get_user_model()
        try:
            token = CLIToken.objects.select_related("user").get(token=self.access_key)
        except CLIToken.DoesNotExist:
            print("doesn't exists")
            return None
        self.user_id = token.user.pk
        return token

    def _validate_username(self, token):
        print("validate username:", self.username, token.user.username)
        return self.username == token.user.username

    def has_valid_credentials(self):
        token = self._fetch_from_db()
        if token is None:
            return False
        return self._validate_username(token)

    def process_request(self):
        valid = True
        if not self.has_valid_credentials():
            valid = False
        return self.user_id, valid
