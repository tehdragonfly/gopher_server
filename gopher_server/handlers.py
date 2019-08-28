import os.path

from dataclasses import dataclass
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


@implementer(IHandler)
@dataclass
class DirectoryHandler:
    """Serves files from a directory, as specified by `base_path`."""
    base_path: str

    def handle(self, selector: str) -> Union[str, bytes]:
        if selector.startswith("/"):
            selector = selector[1:]

        file_path = os.path.abspath(os.path.join(self.base_path, selector))

        if not file_path.startswith(self.base_path):
            raise NotFound

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index")

        if not os.path.isfile(file_path):
            raise NotFound

        with open(file_path) as f:
            return f.read()
