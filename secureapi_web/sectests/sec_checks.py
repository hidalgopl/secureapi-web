import json
import secrets

import logging
import requests

from .service import SecTestResult

FINGERPRINT_HEADERS = (
    "x-powered-by",
    "x-generator",
    "server",
    "x-aspnet-version",
    "x-aspnetmvc-version",
)

FINGERPRINT_COOKIES = ("zope3", "cakephp", "kohanasession", "laravel_session")

log = logging.getLogger(__name__)


def x_content_type_options_nosniff(
    response: requests.Response, client
) -> SecTestResult:
    test_code = "SEC#0001"
    try:
        header = response.headers.get("x-content-type-options")
        if header:
            if header == "nosniff":
                status = "passed"
        else:
            status = "failed"
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def x_frame_options_deny(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0002"
    try:
        header = response.headers.get("x-frame-options")
        if header and header == "deny":
            status = "passed"
        else:
            status = "failed"
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def x_xss_protection(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0003"
    try:
        header = response.headers.get("x-xss-protection")
        if header and header in ["1", "1; mode=block"]:
            status = "passed"
        else:
            status = "failed"
    except Exception as e:
        log.exception(e)
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def content_security_policy(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0004"
    try:
        header = response.headers.get("content-security-policy")
        if header and header in ["default-src 'none'"]:
            status = "passed"
        else:
            status = "failed"
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def options_request_not_allowed(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0005"
    try:
        resp = client.get(response.url)
        if resp.status_code == requests.status_codes.codes.not_allowed:
            status = "passed"
        else:
            status = "failed"
    except Exception as e:
        resp = response
        log.exception(e)
        status = "error"
    return SecTestResult(url=resp.url, test_code=test_code, status=status)


def detect_fingerprint_headers(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0006"
    headers = [h.lower() for h in response.headers.keys()]
    try:
        for header in FINGERPRINT_HEADERS:
            if header in headers:
                status = "failed"
                break
            else:
                status = "passed"
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def detect_fingerprint_cookies(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0007"
    try:
        status = "passed"
        for cookie_name in FINGERPRINT_COOKIES:
            if cookie_name in response.cookies.keys():
                status = "failed"
                break
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def check_cors_setup(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0008"
    try:
        header = response.headers.get("access-control-allow-origin")
        if header and header != "*":
            status = "passed"
        else:
            status = "failed"
    except Exception as e:
        log.exception(e)
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)


def check_if_payload_is_validated(response: requests.Response, client) -> SecTestResult:
    test_code = "SEC#0009"
    random_key, random_val = secrets.token_urlsafe(), secrets.token_hex()
    try:
        random_payload = json.dumps({random_key: random_val})
        resp = client.get(response.url, json=random_payload)
        if resp.status_code != requests.status_codes.codes.bad_request:
            status = "failed"
        else:
            status = "passed"
    except Exception as e:
        status = "error"
    return SecTestResult(url=response.url, test_code=test_code, status=status)
