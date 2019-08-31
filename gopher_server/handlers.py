import os.path

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
class DirectoryHandler:
    """Serves files from a directory, as specified by `base_path`."""

    def __init__(self, base_path):
        self.base_path = os.path.abspath(base_path)

    def handle(self, selector: str) -> Union[str, bytes]:
        # Remove leading slash because os.path.join regards it as a full path
        # otherwise.
        if selector.startswith("/"):
            selector = selector[1:]

        file_path = os.path.abspath(os.path.join(self.base_path, selector))

        # Don't allow breaking out of the base directory.
        if not file_path.startswith(self.base_path):
            raise NotFound

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index")

        if not os.path.isfile(file_path):
            raise NotFound

        with open(file_path) as f:
            return f.read()
