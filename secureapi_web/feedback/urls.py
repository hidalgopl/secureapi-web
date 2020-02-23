from django.urls import path

from secureapi_web.feedback.views import feedback_view

app_name = "feedback"

urlpatterns = [
    path("", feedback_view, name="create-feedback"),
]
