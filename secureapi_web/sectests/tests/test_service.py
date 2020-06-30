import uuid
from typing import List

import pytest
from django.conf import settings

from secureapi_web.sectests.models import SecTestSuite
from secureapi_web.sectests.service import CLIAuthService
from secureapi_web.sectests.tests.factories import UserFactory, CLITokenFactory, SecTestSuiteFactory
from secureapi_web.users.models import CLIToken, User

FREE_SUITES_RUNS = 5


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def cli_token(user) -> CLIToken:
    return CLITokenFactory(user=user)


@pytest.fixture
def sec_test_suites(user) -> List[SecTestSuite]:
    return [SecTestSuiteFactory(user=user, id=uuid.uuid4().hex) for _ in range(0, FREE_SUITES_RUNS + 1)]


@pytest.mark.django_db
def test_service_cli_auth_service_happy_path(cli_token: CLIToken, user: User):
    service = CLIAuthService(
        username=user.username,
        cli_token=cli_token.token
    )
    user_id, is_valid = service.process_request()
    assert user_id == user.id
    assert is_valid


@pytest.mark.django_db
def test_service_limit_exceeded(
    cli_token: CLIToken,
    user: User,
    sec_test_suites: List[SecTestSuite],
    monkeypatch
):
    service = CLIAuthService(
        username=user.username,
        cli_token=cli_token.token
    )
    monkeypatch.setattr(settings, 'FREE_RUNS_LIMITED', True)
    monkeypatch.setattr(settings, 'FREE_RUNS', FREE_SUITES_RUNS)
    user_id, is_valid = service.process_request()
    assert user_id == user.id
    assert is_valid is False
