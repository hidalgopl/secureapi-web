from rest_framework import serializers

from secureapi_web.solutions.models import SecSolution


class SecSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecSolution
        fields = ("code", "solution", "owasp_link")
