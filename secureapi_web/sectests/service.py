import requests


class SecTest:
    TEST_CODE = "SEC#1"

    def __init__(self, resp: requests.Response, client, test_func: function, new_req_required=False):
        self.response = resp  # requests.Response
        self.client = client  # client responsible for getting response, default requests.Client
        self.test_func = test_func
        self.new_request_required = new_req_required

    def run_test(self):
        result = self.test_func(self.response, self.client)
        return result

    def create_report(self, result):
        return {
            "url": result.url,
            "test_code": result.test_code,
            "status": result.status
        }

    def get_result(self):
        result = self.run_test()
        report = self.create_report(result)
        return report


class SecTestResult:
    def __init__(self, url, test_code, status):
        self.url = url
        self.test_code = test_code
        self.status = status
