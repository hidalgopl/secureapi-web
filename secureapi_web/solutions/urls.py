from django.urls import path

from secureapi_web.solutions.views import sec_solution_view

app_name = "solutions"

urlpatterns = [path("all", sec_solution_view, name="sec_solution_list")]
