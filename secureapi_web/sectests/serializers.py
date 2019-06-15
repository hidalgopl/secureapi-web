from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from secureapi_web.sectests.models import SecTest, SecTestSuite


class SecTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecTest
        fields = ('id', 'result', 'error_code')


class SecTestSuiteSerializer(WritableNestedModelSerializer):
    tests = SecTestSerializer(many=True)

    class Meta:
        model = SecTestSuite
        fields = ('tests', 'user', 'security_index')

