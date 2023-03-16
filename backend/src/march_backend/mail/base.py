"""Base mail classes to inherit from."""
from imaplib import IMAP4


class BaseMailProvider:
    """Basic Mail Provider to inherit from"""

    def get_connection(self, username: str, secret: str) -> IMAP4:
        """Get the IMAP4 connection."""
        connection = IMAP4()
        connection.login(username, secret)
        return connection

    def search(self, term, username, secret):
        """Search for emails."""
        connection = self.get_connection(username, secret)
        return connection.search(term)
