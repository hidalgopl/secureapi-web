from django.conf.urls import url
from django.urls import path

from secureapi_web.users.views import (
    cli_token_view,
    user_profile_view,
    exchange_token,
    get_access_token,
)

app_name = "users"
urlpatterns = [
    url(r"code/", view=get_access_token, name="code-exchange"),
    path("settings", view=cli_token_view, name="settings"),
    path("profile", view=user_profile_view, name="profile"),
    url(r"social/(?P<backend>[^/]+)/$", exchange_token),
]
