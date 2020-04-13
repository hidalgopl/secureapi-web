from django.conf.urls import url
from django.urls import path

from secureapi_web.users.views import (
    test_list_view,
    user_detail_view,
    cli_token_view,
    user_profile_view,
    exchange_token,
    get_access_token,
)

app_name = "users"
urlpatterns = [
    url(r"code/", view=get_access_token, name="code-exchange"),
    # path("", view=user_list_view, name="list"),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("test", view=test_list_view, name="tests"),
    path("settings", view=cli_token_view, name="settings"),
    path("profile", view=user_profile_view, name="profile"),
    url(r"social/(?P<backend>[^/]+)/$", exchange_token),
]
