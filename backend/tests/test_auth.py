"""Tests for march_backend.auth"""
import json
from unittest.mock import MagicMock, mock_open

import pytest

from march_backend import auth
from march_backend.auth import get_google_session, oauth_start

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="secret")
def fixture_secret():
    """client_secret.json fixture"""
    with open("test_secret.json", "rt", encoding="utf-8") as sec_f:
        test_secret = sec_f.read()
    return test_secret


class TestGetGoogleSession:
    """Test get_google_session"""

    async def test_default(self, mocker):
        """Test get_google_session"""
        with open("test_secret.json", "rt", encoding="utf-8") as sec_f:
            test_secret = sec_f.read()
        secret = json.loads(test_secret)["web"]
        mock_oauth2session = mocker.patch.object(auth, "OAuth2Session")
        openmock = mock_open(read_data=test_secret)

        mocker.patch.object(auth, "open", openmock)
        await get_google_session()
        openmock.assert_called_once_with("client_secret.json", "rt", encoding="utf-8")
        mock_oauth2session.assert_called_once_with(
            client_id=secret["client_id"],
            redirect_uri=secret["redirect_uris"][0],
            scope=[
                "https://mail.google.com/",
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            state=None,
        )

    async def test_with_state(self, mocker, secret):
        """state should be passed to OAuth2Session"""
        test_secret = secret
        secret = json.loads(secret)["web"]
        mock_oauth2session = mocker.patch.object(auth, "OAuth2Session")
        openmock = mock_open(read_data=test_secret)

        mocker.patch.object(auth, "open", openmock)
        await get_google_session(state="bla")
        openmock.assert_called_once_with("client_secret.json", "rt", encoding="utf-8")
        mock_oauth2session.assert_called_once_with(
            client_id=secret["client_id"],
            redirect_uri=secret["redirect_uris"][0],
            scope=[
                "https://mail.google.com/",
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            state="bla",
        )


class MockGoogleSession:
    """Mock Google OAuth2 Session"""

    authorization_url = MagicMock(return_value=["bla"])


class TestOAuthStart:
    """Test oauth_start"""

    async def test_default(self, mocker, secret):
        """Test default behaviour"""
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_google = MockGoogleSession()
        secret = json.loads(secret)["web"]
        mock_get_google_session.return_value = (
            mock_google,
            secret,
        )
        res = await oauth_start()
        mock_get_google_session.assert_called_once_with()
        mock_google.authorization_url.assert_called_once_with(
            secret["auth_uri"], access_type="offline", prompt="select_account"
        )
        assert res == mock_google.authorization_url.return_value[0]
