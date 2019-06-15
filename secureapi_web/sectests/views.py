from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.sectests.serializers import SecTestSerializer, SecTestSuiteSerializer


class MyTestsView(ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('result', 'security_index')

    def get_queryset(self):
        return SecTestSuite.objects.filter(user=self.request.user).all()


my_tests_view = MyTestsView.as_view()


class TestDetailView(ModelViewSet):
    serializer_class = SecTestSerializer


test_detail_view = TestDetailView.as_view({'get': 'retrieve', 'post': 'create'})


class TestSuiteView(CreateAPIView):
    serializer_class = SecTestSuiteSerializer





test_suite_view = TestSuiteView.as_view()
