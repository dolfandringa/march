"""Tests for march_backend.auth"""
# pylint: disable=duplicate-code
import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open

import pytest
from fastapi import HTTPException

from march_backend import auth
from march_backend.auth import get_google_session, oauth_start, oauth_token

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="secret")
def fixture_secret():
    """client_secret.json fixture"""
    fname = Path(__file__).parent / "test_secret.json"
    with fname.open("rt", encoding="utf-8") as sec_f:
        test_secret = sec_f.read()
    return test_secret


class TestGetGoogleSession:
    """Test get_google_session"""

    async def test_default(self, mocker, secret):
        """Test get_google_session"""
        test_secret = secret
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


class MockGoogleSession:  # pylint: disable=too-few-public-methods
    """Mock Google OAuth2 Session"""

    authorization_url = MagicMock(return_value=["bla"])
    fetch_token = MagicMock(return_value="Fake token")


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

    async def test_get_google_session_error(self, mocker):
        """
        Test that a 403 Forbidden exception was raised
        on get_google_session errors.
        """
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_get_google_session.side_effect = TypeError("Test")
        with pytest.raises(HTTPException) as exc:
            await oauth_start()
        assert exc.value.status_code == 403

    async def test_authorization_url_error(self, mocker, secret):
        """
        Test that a 403 Forbidden exception was raised
        on google.authorization_url errors.
        """
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_google = MockGoogleSession()
        mock_google.authorization_url.side_effect = TypeError("Test")
        secret = json.loads(secret)["web"]
        mock_get_google_session.return_value = (
            mock_google,
            secret,
        )
        with pytest.raises(HTTPException) as exc:
            await oauth_start()
        assert exc.value.status_code == 403


class TestOAuthToken:
    """Test oauth_token"""

    async def test_default(self, mocker, secret):
        """Test default behaviour"""
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_google = MockGoogleSession()
        secret = json.loads(secret)["web"]
        mock_get_google_session.return_value = (
            mock_google,
            secret,
        )
        res = await oauth_token("state", "code")
        mock_get_google_session.assert_called_once_with(state="state")
        mock_google.fetch_token.assert_called_once_with(
            secret["token_uri"], client_secret=secret["client_secret"], code="code"
        )
        assert res == mock_google.fetch_token.return_value

    async def test_get_google_session_error(self, mocker):
        """
        Test that a 403 Forbidden exception was raised
        on get_google_session errors.
        """
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_get_google_session.side_effect = TypeError("Test")
        with pytest.raises(HTTPException) as exc:
            await oauth_token("state", "code")
        assert exc.value.status_code == 403

    async def test_fetch_token_error(self, mocker, secret):
        """
        Test that a 403 Forbidden exception was raised
        on google.fetch_token errors.
        """
        mock_get_google_session = mocker.patch.object(auth, "get_google_session")
        mock_google = MockGoogleSession()
        mock_google.fetch_token.side_effect = TypeError("Test")
        secret = json.loads(secret)["web"]
        mock_get_google_session.return_value = (
            mock_google,
            secret,
        )
        with pytest.raises(HTTPException) as exc:
            await oauth_token("state", "code")
        assert exc.value.status_code == 403
