from django_filters import rest_framework as filters

from rest_framework.generics import ListAPIView

from secureapi_web.sectests.models import SecTestSuite


class MyTestsView(ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('result', 'security_index')

    def get_queryset(self):
        return SecTestSuite.objects.filter(user=self.request.user).all()
