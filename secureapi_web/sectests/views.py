from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.sectests.serializers import SecTestSuiteSerializer, CLIAuthSerializer
from secureapi_web.sectests.service import CLIAuthService


class MyTestsView(ListAPIView):
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('result',)
    serializer_class = SecTestSuiteSerializer

    def get_queryset(self):
        qs = (
            SecTestSuite.objects.prefetch_related("sectest_set")
            .select_related("user")
            .filter(user=self.request.user)
        )
        return qs


my_tests_view = MyTestsView.as_view()


class CLIAuthView(APIView):
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
            data={"user_id": user_id, "is_allowed": valid, "remain_limit": "234"},
        )


cli_auth_view = CLIAuthView.as_view()
