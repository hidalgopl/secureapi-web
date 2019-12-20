from rest_framework import serializers

from secureapi_web.users.models import CLIToken


class CLITokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIToken
        fields = ("token",)
