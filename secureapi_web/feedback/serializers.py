from rest_framework import serializers

from secureapi_web.feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = (
            "ease_of_use",
            "likeliness_of_recommend",
            "overall_score",
            "proposed_price",
            "open_feedback",
            "user"
        )
