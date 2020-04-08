from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.sectests.serializers import SecTestSuiteSerializer, CLIAuthSerializer
from secureapi_web.sectests.service import CLIAuthService


class MyTestsView(ListAPIView):
    """
    Returns paginated list of user's tests.
    """
    serializer_class = SecTestSuiteSerializer

    def get_queryset(self):
        qs = (
            SecTestSuite.objects.prefetch_related("sectest_set")
            .select_related("user")
            .filter(user=self.request.user.pk)
        )

        return qs


my_tests_view = MyTestsView.as_view()


class SecTestSuiteDetailsView(RetrieveAPIView):
    """
    Returns details for test suite.
    """
    serializer_class = SecTestSuiteSerializer

    def get_queryset(self):
        qs = SecTestSuite.objects.filter(user=self.request.user)
        return qs


sec_test_suite_details_view = SecTestSuiteDetailsView.as_view()


class CLIAuthView(APIView):
    """
    Endpoint used for CLI tool authentication.
    """
    serializer_class = CLIAuthSerializer

    def post(self, request):
        serializer = CLIAuthSerializer(data=request.data)
        serializer.is_valid()
        service = CLIAuthService(
            username=serializer.data["username"],
            cli_token=serializer.data["access_key"],
        )
        user_id, valid = service.process_request()
        status_code = status.HTTP_200_OK if valid else status.HTTP_401_UNAUTHORIZED
        return JsonResponse(
            status=status_code,
            data={"user_id": user_id, "is_allowed": valid},
        )


cli_auth_view = CLIAuthView.as_view()
