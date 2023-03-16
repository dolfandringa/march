"""GMail classes"""
import imaplib
from base64 import b64encode
from imaplib import IMAP4_SSL

from fastapi import APIRouter

from ..exceptions import PermissionDeniedError
from .base import BaseMailProvider

router = APIRouter()


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
        try:
            connection.authenticate("XOAUTH2", lambda _: auth_string)
        except imaplib.IMAP4.error as exc:
            raise PermissionDeniedError(
                "Permission denied when authenticating"
            ) from exc
        return connection


@router.get("/search", tags=["mail", "gmail"])
async def search(query: str, username: str, token: str) -> str:
    """Search gmail."""
    provider = GMailProvider()
    provider.search(query, username, token)
    return "There you go!"
