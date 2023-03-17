"""Base mail classes to inherit from."""
import imaplib
import logging
from email import message_from_string
from email.message import Message
from imaplib import IMAP4
from typing import AsyncIterator, List

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

    async def fetch(self, ids: List[int], connection: IMAP4) -> AsyncIterator[Message]:
        """Fetch emails by ids."""
        log = logging.getLogger(__name__)
        for mid in ids:
            message = connection.fetch(str(mid), "(RFC822)")[1]
            log.debug("Got message %s", message)
            yield message_from_string(str(message))

    async def search(self, query: str, username: str, secret: str) -> List[Message]:
        """Search for emails."""
        log = logging.getLogger(__name__)
        connection = self.get_connection(username, secret)
        log.debug("Connection established. Capability: %s", connection.PROTOCOL_VERSION)
        inboxes = connection.list()[1]
        log.debug(inboxes)
        connection.select(mailbox="INBOX")
        res = connection.search(None, query)
        if res[0] != "OK":
            log.error("Unexpected error executing search %s", res)
            raise RuntimeError("Unkown error executing search")
        ids = res[1][0].decode("utf-8").split()
        log.debug("ids: %s", ids)
        return [message async for message in self.fetch(ids, connection)]


@router.get("/search", tags=["mail"])
async def search(username: str, password: str, query: str):
    """Search and return emails based on query."""
    provider = BaseMailProvider()
    res = provider.search(query, username, password)
    return res
