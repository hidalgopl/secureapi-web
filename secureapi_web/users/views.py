from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from rest_framework.generics import RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from secureapi_web.sectests.models import SecTest
from secureapi_web.users.models import CLIToken
from secureapi_web.users.serializers import CLITokenSerializer, UserProfileSerializer

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class TestListView(LoginRequiredMixin, ListView):

    model = SecTest
    # slug_field = "username"
    # slug_url_kwarg = "username"
    template_name = "users/user_tests.html"


test_list_view = TestListView.as_view()


class UserCLITokenView(RetrieveDestroyAPIView):
    serializer_class = CLITokenSerializer

    def get_object(self):
        print(f"user: {self.request.user}")
        return CLIToken.objects.get(user=self.request.user)


cli_token_view = UserCLITokenView.as_view()


class UserProfileView(RetrieveUpdateAPIView):
    """
    Return user profile. Used on user settings page. Supports also updates in profile.
    """
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


user_profile_view = UserProfileView.as_view()


class MockUserProfileView(APIView):
    def get(self, request):
        return Response(
            {
                "username": "oskarro",
                "email": "oskar@orzelowski.pl",
                "first_name": "Oskar",
                "last_name": "Orzełowski",
                "company": "thirty3",
                "password":  "******",
                "access_key": "my access key"
            }, headers={'Access-Control-Allow-Origin': '*', "Content-Type": "application/json"}
        )


mock_user_profile = MockUserProfileView.as_view()
