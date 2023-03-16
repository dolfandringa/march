"""GMail classes"""
from base64 import b64encode
from imaplib import IMAP4_SSL

from .base import BaseMailProvider


class GMailProvider(BaseMailProvider):
    """GMail mail provider"""

    def get_connection(self, username: str, secret: str) -> IMAP4_SSL:
        """
        Get the connection using OAuth2 token.
        """
        connection = IMAP4_SSL("imap.google.com")
        auth_string = b64encode(
            f"user={username}\1auth=Bearer {secret}\1\1".encode("utf-8")
        )
        connection.authenticate("XOAUTH2", lambda _: auth_string)
        return connection
