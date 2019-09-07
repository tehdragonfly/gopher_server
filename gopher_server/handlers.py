import os.path
import re

from typing import Union
from zope.interface import Interface, implementer

from gopher_server.menu import Menu


class NotFound(Exception):
    pass


class IHandler(Interface):
    async def handle(self, selector: str) -> Union[str, bytes, Menu]:
        """
        Receives a selector as a string, and returns the response as either a
        a string (for text responses), bytes (for binary responses), or a Menu
        object.
        """
        pass


@implementer(IHandler)
class DirectoryHandler:
    """Serves files from a directory, as specified by `base_path`."""

    def __init__(self, base_path):
        self.base_path = os.path.abspath(base_path)

    async def handle(self, selector: str) -> Union[str, bytes]:
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


@implementer(IHandler)
class PatternHandler:
    """Uses pattern matching to map selectors to view functions."""

    def __init__(self):
        self.patterns = []

    async def handle(self, selector: str) -> Union[str, bytes]:
        for pattern, func in self.patterns:
            match = pattern.match(selector)
            if match:
                return func(selector, **match.groupdict())
        raise NotFound

    def register(self, pattern):
        pattern = re.compile("^%s$" % pattern)

        def f(func):
            self.patterns.append((pattern, func))
            return func

        return f
