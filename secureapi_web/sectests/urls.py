from django.urls import path

from secureapi_web.sectests.views import (
    my_tests_view, test_runner, cli_auth_view)

app_name = "sectests"

urlpatterns = [
    path("my/sec-tests/", my_tests_view, name="my_tests"),
    path("auth", cli_auth_view, name="cli-auth"),
    path("run", test_runner, name="runner")
]
