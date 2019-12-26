from rest_framework.generics import ListAPIView

from secureapi_web.solutions.models import SecSolution
from secureapi_web.solutions.serializers import SecSolutionSerializer


class SecSolutionView(ListAPIView):
    queryset = SecSolution.objects.all()
    serializer_class = SecSolutionSerializer

    def filter_queryset(self, queryset):
        # for /solutions?sec_codes=SEC001,SEC002 etc.
        sec_codes = self.request.query_params.get("sec_codes", ",")
        print(sec_codes)
        sec_codes = sec_codes.split(",")
        print(f"splitted: {sec_codes}")
        print(f"qs len: {len(queryset)}")
        qs = queryset.filter(code__in=sec_codes)
        print(f"qs len: {len(qs)}")
        return qs


sec_solution_view = SecSolutionView.as_view()
