from rest_framework.serializers import ModelSerializer, SerializerMethodField

from secureapi_web.sectests.models import SecTestSuite, SecTest


class SecTestSerializer(ModelSerializer):
    class Meta:
        model = SecTest
        fields = ("id", "result", "code")


class SecTestSuiteSerializer(ModelSerializer):
    tests = SerializerMethodField()

    def get_tests(self, obj):
        tests = obj.sectest_set.all()
        return SecTestSerializer(tests, many=True).data

    class Meta:
        model = SecTestSuite
        fields = ("id", "url", "tests")
