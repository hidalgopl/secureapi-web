from secrets import token_urlsafe


def cli_token_gen():
    return token_urlsafe(27)
