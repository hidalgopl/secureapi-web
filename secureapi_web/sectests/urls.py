from django.urls import path

from secureapi_web.sectests.views import (
    test_detail_view,

    test_suite_view, my_tests_view)

app_name = "sectests"

urlpatterns = [
    path("my/sec-tests/", my_tests_view, name="my_tests"),
    path("sec-test/<int: id>/", test_detail_view, name="test_detail"),
    path("sec-test/", view=test_suite_view, name="sec_test_suite"),
]
