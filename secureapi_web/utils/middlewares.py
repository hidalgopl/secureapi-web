from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        self.content_security_policy = settings.CONTENT_SECURITY_POLICY
        self.cache_control_max_age = settings.CACHE_CONTROL_MAX_AGE

    def process_response(self, request, response):
        if self.content_security_policy and 'content-security-policy' not in response:
            response["Content-Security-Policy"] = self.content_security_policy
        if self.cache_control_max_age and 'cache-control' not in response:
            response["Cache-Control"] = self.cache_control_max_age

        return response
