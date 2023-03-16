"""Base mail classes to inherit from."""
import imaplib
from imaplib import IMAP4

from fastapi import APIRouter

from ..exceptions import PermissionDeniedError

router = APIRouter()


class BaseMailProvider:
    """Basic Mail Provider to inherit from"""

    def get_connection(self, username: str, secret: str) -> IMAP4:
        """Get the IMAP4 connection."""
        connection = IMAP4()
        print(f"connection.error: {connection.error} {type(connection.error)}")
        try:
            connection.login(username, secret)
        except imaplib.IMAP4.error as exc:
            # use the fully qualified class path else unittests will see a MagicMock
            raise PermissionDeniedError(
                "Permission denied when trying to login."
            ) from exc
        return connection

    def search(self, term, username, secret):
        """Search for emails."""
        connection = self.get_connection(username, secret)
        return connection.search(term)


@router.get("/search", tags=["mail"])
async def search(username: str, password: str, query: str) -> str:
    """Search and return emails based on query."""
    provider = BaseMailProvider()
    provider.search(query, username, password)
    return "There you go"
