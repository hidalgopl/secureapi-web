from django.urls import path

from secureapi_web.sectests.views import my_tests_view, cli_auth_view, sec_test_suite_details_view

app_name = "sectests"

urlpatterns = [
    path("my", my_tests_view, name="my_tests"),
    path("suites/<pk>", sec_test_suite_details_view, "suite_details"),
    path("auth", cli_auth_view, name="cli-auth"),
]
