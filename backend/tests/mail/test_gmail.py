"""Test GMail class"""

from imaplib import IMAP4_SSL

import pytest

from march_backend.exceptions import PermissionDeniedError
from march_backend.mail import gmail


@pytest.fixture(name="imap")
def imap_fixture(mocker):
    """Fixture to return and mock GMailProvider"""
    mock_imap4 = mocker.patch("march_backend.mail.gmail.IMAP4_SSL")
    mocker.patch.object(mock_imap4, "open")
    connection = mock_imap4.return_value
    provider = gmail.GMailProvider()
    return (provider, connection, mock_imap4)


class TestGMailProvider:
    """Test GMailProvider"""

    def test_get_connection(self, mocker, imap):
        """test get_connection."""
        username = "roger.rabbit@gmail.com"
        token = "versecret"
        auth_string = f"user={username}\1auth=Bearer {token}\1\1"
        provider, connection, mock_imap4 = imap
        mock_auth = mocker.patch.object(connection, "authenticate")
        mock_auth.return_value = "OK", ""
        provider.get_connection(username, token)
        mock_auth.assert_called_once()
        print(f"calls: {mock_auth.calls}")
        assert mock_auth.call_args[0][0] == "XOAUTH2"
        assert mock_auth.call_args[0][1]("bla") == auth_string.encode("utf-8")
        mock_imap4.assert_called_once_with(host="imap.gmail.com")

    def test_get_connection_error(self, mocker, imap):
        """test get_connection when raising an imap error."""
        username = "dolf"
        token = "secret"
        auth_string = f"user={username}\1auth=Bearer {token}\1\1"
        provider, connection, _ = imap
        mock_auth = mocker.patch.object(connection, "authenticate")
        mock_auth.side_effect = IMAP4_SSL.error("Permission denied")
        with pytest.raises(PermissionDeniedError):
            provider.get_connection(username, token)
        mock_auth.assert_called_once()
        assert mock_auth.call_args[0][0] == "XOAUTH2"
        assert mock_auth.call_args[0][1]("bla") == auth_string.encode("utf-8")
