"""Test Base Mail classes"""

from imaplib import IMAP4

import pytest

from march_backend.exceptions import PermissionDeniedError
from march_backend.mail import base


@pytest.fixture(name="imap")
def imap_fixture(mocker):
    """Fixture to return and mock BaseMailProvider"""
    mock_imap4 = mocker.patch("march_backend.mail.base.IMAP4")
    mocker.patch.object(mock_imap4, "open")
    connection = mock_imap4.return_value
    provider = base.BaseMailProvider()
    return (provider, connection)


class TestBaseMailProvider:
    """Test BaseMailProvider"""

    def test_get_connection(self, mocker, imap):
        """test get_connection."""
        username = "dolf"
        password = "secret"
        provider, connection = imap
        mock_login = mocker.patch.object(connection, "login")
        mock_login.return_value = "OK", ""
        provider.get_connection(username, password)
        connection.login.assert_called_once_with(username, password)

    def test_get_connection_error(self, mocker, imap):
        """test get_connection when raising an imap error."""
        username = "dolf"
        password = "secret"
        provider, connection = imap
        mock_login = mocker.patch.object(connection, "login")
        mock_login.side_effect = IMAP4.error("Permission denied")
        with pytest.raises(PermissionDeniedError):
            provider.get_connection(username, password)
        connection.login.assert_called_once_with(username, password)

    def test_search(self, mocker, imap):
        """test search"""
        username = "dolf"
        password = "secret"
        provider, connection = imap
        mock_get_connection = mocker.patch.object(provider, "get_connection")
        mock_get_connection.return_value = connection
        mock_search = mocker.patch.object(connection, "search")
        provider.search("Something", username, password)
        mock_get_connection.assert_called_once_with(username, password)
        mock_search.assert_called_once_with("Something")
