from secureapi_web.users.models import CLIToken, User


def create_cli_token(backend, details, user=None, *args, **kwargs):
    user = User.objects.get(username=details["username"])
    CLIToken.objects.create(user=user)
