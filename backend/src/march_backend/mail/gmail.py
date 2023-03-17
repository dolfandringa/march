"""GMail classes"""
import imaplib
import logging
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
        log = logging.getLogger(__name__)
        connection = IMAP4_SSL(host="imap.gmail.com")
        auth_string = f"user={username}\1auth=Bearer {secret}\1\1".encode("utf-8")
        try:
            log.debug("auth_string: %s", auth_string)
            connection.authenticate("XOAUTH2", lambda _: auth_string)
        except imaplib.IMAP4.error as exc:
            raise PermissionDeniedError(
                f"Permission denied when authenticating: {exc}"
            ) from exc
        return connection


@router.get("/search", tags=["mail", "gmail"])
async def search(query: str, username: str, token: str):
    """Search gmail."""
    provider = GMailProvider()
    res = provider.search(query, username, token)
    return res
