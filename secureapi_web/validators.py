from django.core.exceptions import ValidationError
import re


def sec_test_code_validator(value):
    if not re.match("SEC#([0-9])\w+", value):
        raise ValidationError("wrong sec test code")
