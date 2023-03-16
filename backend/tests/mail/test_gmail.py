"""Test GMail class"""

from base64 import b64encode

import pytest

from march_backend.mail import gmail


@pytest.fixture(name="imap")
def imap_fixture(mocker):
    """Fixture to return and mock GMailProvider"""
    mock_imap4 = mocker.patch("march_backend.mail.gmail.IMAP4_SSL")
    mocker.patch.object(mock_imap4, "open")
    connection = mock_imap4.return_value
    provider = gmail.GMailProvider()
    return (provider, connection)


class TestGMailProvider:
    """Test GMailProvider"""

    def test_get_connection(self, mocker, imap):
        """test get_connection."""
        username = "roger.rabbit@gmail.com"
        token = "versecret"
        auth_string = f"user={username}\1auth=Bearer {token}\1\1"
        provider, connection = imap
        spy_b64encode = mocker.patch("march_backend.mail.gmail.b64encode")
        spy_b64encode.return_value = b64encode(auth_string.encode("utf-8"))
        mock_auth = mocker.patch.object(connection, "authenticate")
        mock_auth.return_value = "OK", ""
        provider.get_connection(username, token)
        spy_b64encode.assert_called_once_with(auth_string.encode("utf-8"))
        mock_auth.assert_called_once()
        print(f"calls: {mock_auth.calls}")
        assert mock_auth.call_args[0][0] == "XOAUTH2"
        assert mock_auth.call_args[0][1]("bla") == spy_b64encode.return_value

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
