from django.urls import path

from secureapi_web.sectests.views import (
    my_tests_view, fake_basic_auth_view, test_runner)

app_name = "sectests"

urlpatterns = [
    path("my/sec-tests/", my_tests_view, name="my_tests"),
    path("auth", fake_basic_auth_view, name="fake-basic-auth"),
    path("run", test_runner, name="runner")
]
