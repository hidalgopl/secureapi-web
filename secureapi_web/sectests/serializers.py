from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
)

from secureapi_web.sectests.models import SecTestSuite, SecTest


class SecTestSerializer(ModelSerializer):
    class Meta:
        model = SecTest
        fields = ("id", "result", "code", "created")


class SecTestSuiteSerializer(ModelSerializer):
    tests = SerializerMethodField()

    def get_tests(self, obj):
        tests = obj.sectest_set.filter(result=1)
        return SecTestSerializer(tests, many=True).data

    class Meta:
        model = SecTestSuite
        fields = ("id", "url", "tests", "user")


class CLIAuthSerializer(Serializer):
    username = serializers.CharField()
    access_key = serializers.CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
