from typing import Union
from zope.interface import Interface, implementer


class NotFound(Exception):
    pass


class IHandler(Interface):
    def handle(self, selector: str) -> Union[str, bytes]:
        """
        Receives a selector as a string, and returns the response as either a
        a string (for text responses) or bytes (for binary responses).
        """
        pass
