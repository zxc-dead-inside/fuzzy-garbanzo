import pytest

from rest_framework.test import APIClient

from market.users.models import User
from market.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db) -> User:
    return UserFactory(password='testpass')


@pytest.fixture
def authenticated_client(user: User, api_client: APIClient) -> APIClient:
    api_client.login(email=user.email, password='testpass')
    return api_client
