from rest_framework.generics import CreateAPIView

from secureapi_web.feedback.models import Feedback
from secureapi_web.feedback.serializers import FeedbackSerializer
from secureapi_web.sectests.service import CLIAuth


class FeedbackView(CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes = (CLIAuth,)


feedback_view = FeedbackView.as_view()
