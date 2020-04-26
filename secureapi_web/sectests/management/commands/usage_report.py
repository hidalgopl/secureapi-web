import json
from datetime import datetime, timedelta

import boto3
from django.conf import settings
from django.core.management.base import BaseCommand

from secureapi_web.sectests.models import SecTestSuite


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):
        parser.add_argument("--last-days", dest="last_days", type=int)
        parser.add_argument("--output", dest="output", type=str)

    def handle(self, *args, **options):
        days_back = options["last_days"]
        since = datetime.utcnow() - timedelta(days=days_back)
        file_name = f"usage_{since.date()}_{datetime.utcnow().date()}.json"
        test_suites = SecTestSuite.objects.filter(created__gte=since).prefetch_related("sectest_set")
        processed_data = self._process_data(test_suites)
        self.report(processed_data, file_name, options.get("output", "stdout"))

    def report(self, processed_data, file_name, output):
        if output == "stdout":
            self.stdout.write(self.style.SUCCESS(processed_data))
        elif output == "s3":
            self._create_report(processed_data, file_name)
            report_url = self._upload_report(file_name)
            self.stdout.write(self.style.SUCCESS(f"Report uploaded to: {report_url}"))

    def _get_tmp_filepath(self, file_name):
        return f"/tmp/{file_name}"

    def _create_report(self, processed_data, file_name):
        file_path = self._get_tmp_filepath(file_name)
        with open(file_path, "w") as tmpfile:
            json.dump(processed_data, tmpfile)
        return file_path

    def _process_data(self, test_suites):
        processed_data = {}
        for test_suite in test_suites:
            try:
                processed_data[test_suite.user.username]["runners"].add(test_suite.origin)
                processed_data[test_suite.user.username].update({
                    "test_suites": processed_data[test_suite.user.username]["test_suites"] + 1,
                    "failed_tests": processed_data[test_suite.user.username]["failed_tests"] + test_suite.sectest_set.filter(result=1).count()
                })
            except KeyError:
                processed_data[test_suite.user.username] = {
                    "test_suites": 1,
                    "runners": {test_suite.origin},
                    "failed_tests": test_suite.sectest_set.filter(result=1).count()
                }
        for user, user_data in processed_data.items():
            user_data["runners"] = list(user_data["runners"])
            processed_data[user] = user_data
            percentage = (user_data["failed_tests"] * 100) / (user_data["test_suites"] * 9)
            user_data["failures"] = f"Failed tests: {percentage:.2f}%"
        return processed_data

    def _upload_report(self, file_name):
        bucket_name = "reports"
        file_path = self._get_tmp_filepath(file_name)
        client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        with open(file_path, "rb") as f:
            client.upload_fileobj(f, bucket_name)

        bucket_location = client.get_bucket_location(Bucket=bucket_name)
        return f"https://s3-{bucket_location['LocationConstraint']}.amazonaws.com/{bucket_name}/{file_name}"
