from rest_framework import serializers

from secureapi_web.users.models import CLIToken, User


class CLITokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLIToken
        fields = ("token",)


class UserProfileSerializer(serializers.ModelSerializer):
    access_key = serializers.SerializerMethodField()

    def get_access_key(self, obj):
        return obj.clitoken_set.last().token

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "access_key")
