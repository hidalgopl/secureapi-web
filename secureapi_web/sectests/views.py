from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import ListAPIView

from secureapi_web.sectests.serializers import SecTestSuiteSerializer
from secureapi_web.sectests.models import SecTestSuite

from basicauth.decorators import basic_auth_required


class MyTestsView(ListAPIView):
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('result',)
    serializer_class = SecTestSuiteSerializer

    def get_queryset(self):
        return SecTestSuite.objects.all()


my_tests_view = MyTestsView.as_view()


@basic_auth_required
def fake_basic_auth_view(request):
    return JsonResponse(
        {"is_allowed": True, "remain_limit": "234"}
    )


@authentication_classes([])
@permission_classes([])
def test_runner(request):
    return JsonResponse({"subject": "test.4.*.complete"})
