"""Test Base Mail classes"""

from email import message_from_string
from imaplib import IMAP4
from unittest.mock import call

import pytest

from march_backend.exceptions import PermissionDeniedError
from march_backend.mail import base

pytestmark = pytest.mark.asyncio


@pytest.fixture(name="imap")
def imap_fixture(mocker):
    """Fixture to return and mock BaseMailProvider"""
    mock_imap4 = mocker.patch("march_backend.mail.base.IMAP4")
    mocker.patch.object(mock_imap4, "open")
    connection = mock_imap4.return_value
    provider = base.BaseMailProvider()
    return (provider, connection)


@pytest.fixture(name="rfc822_email")
def email_fixture():
    """RFC822 email string."""
    return (
        """From: John Smith <john.smith@example.com>\r\n"""
        """To: Jane Doe <jane.doe@example.com>\r\n"""
        """Subject: Example Email\r\n"""
        """Date: Thu, 17 Mar 2023 12:30:00 -0500\r\n"""
        """Message-ID: <1234@example.com>\r\n\r\n"""
        """Hello Jane,\r\n\r\nI hope this email finds you well."""
        """I just wanted to reach out and say hello and see how you're doing. """
        """It's been a while since we last spoke, and I wanted to catch up.\r\n\r\n"""
        """Best regards,\r\n\r\nJohn"""
    )


class AsyncIterator:
    """Wrapper to make a sequence into an async iterator."""

    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as exc:
            raise StopAsyncIteration from exc


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

    async def test_fetch(self, mocker, imap, rfc822_email: str):
        """Test fetching and individual mail."""
        ids = [1, 25, 12, 34]
        calls = [call(str(id), "(RFC822)") for id in ids]
        provider, connection = imap
        mock_fetch = mocker.patch.object(connection, "fetch")
        messages = [rfc822_email] * len(ids)
        mock_fetch.side_effect = [("OK", message) for message in messages]
        actual = [dict(message) async for message in provider.fetch(ids, connection)]
        assert mock_fetch.mock_calls == calls
        assert actual == [dict(message_from_string(m)) for m in messages]

    async def test_search(
        self, mocker, imap, rfc822_email
    ):  # pylint: disable=too-many-locals
        """test search"""
        username = "dolf"
        password = "secret"
        provider, connection = imap
        mock_get_connection = mocker.patch.object(provider, "get_connection")
        mock_get_connection.return_value = connection
        mock_list = mocker.patch.object(connection, "list")
        mock_list.return_value = (b"OK", [b"bla", b"INBOX", b"test"])
        mock_select = mocker.patch.object(connection, "select")
        mock_search = mocker.patch.object(connection, "search")
        ids = [b"1 25 12 34"]
        expected = [
            dict(message_from_string(m))
            for m in [rfc822_email] * len(ids[0].decode("utf-8").split())
        ]
        mock_search.return_value = ("OK", ids)
        mock_fetch = mocker.patch.object(provider, "fetch")
        mock_fetch.return_value = AsyncIterator(expected)
        actual = [
            dict(message)
            for message in await provider.search("Something", username, password)
        ]
        mock_get_connection.assert_called_once_with(username, password)
        mock_list.assert_called_once_with()
        mock_select.assert_called_once_with(mailbox="INBOX")
        mock_search.assert_called_once_with(None, "Something")
        mock_fetch.assert_called_with(ids[0].decode("utf-8").split(), connection)
        assert actual == expected
