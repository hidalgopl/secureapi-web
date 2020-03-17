from json import JSONDecodeError

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from requests.exceptions import HTTPError
from social_core.backends.github import GithubOAuth2
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from social_django.utils import psa
from social_core.exceptions import AuthForbidden
from logging import getLogger

from secureapi_web.sectests.models import SecTest
from secureapi_web.users.models import CLIToken
from secureapi_web.users.serializers import CLITokenSerializer, UserProfileSerializer, SocialSerializer, CodeSerializer

User = get_user_model()
log = getLogger(__name__)

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


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.
    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.
    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'
    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.
    ## Request format
    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except AuthForbidden as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExchangeCodetoAccessTokenView(APIView):
    """

         Requests must include the following field
        - `code`: The OAuth2 code provided by github
        - `state`: random string used in 1st step of Oauth
        """
    permission_classes = (AllowAny,)
    authentication_classes = ()
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # set up non-field errors key
            # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
            nfe = 'non_field_errors'
            try:
                body = {
                    "client_id": settings.SOCIAL_AUTH_GITHUB_KEY,
                    "client_secret": settings.SOCIAL_AUTH_GITHUB_SECRET,
                    "code": serializer.validated_data["code"],
                    "state": serializer.validated_data["state"],
                    "redirect_uri": settings.GITHUB_REDIRECT_URI

                }
                resp = requests.post(
                    GithubOAuth2.ACCESS_TOKEN_URL,
                    data=body,
                    headers={"Accept": "application/json"}
                )
                print(resp.content)
                access_token = resp.json()["access_token"]

                return Response(
                    {"access_token": access_token}
                )

            except (KeyError, JSONDecodeError) as e:
                print(e)
                log.info(resp.content)
                return Response(
                    {'errors': {nfe: 'access_token not found in github resp'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response()


get_access_token = ExchangeCodetoAccessTokenView.as_view()




