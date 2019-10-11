import os.path
import re

from typing import Union
from zope.interface import Interface, implementer

from gopher_server.menu import Menu


class NotFound(Exception):
    pass


class IHandler(Interface):
    """
    Interface for handler classes.

    A handler is called by the :class:`Application <gopher_server.application.Application>`,
    and is responsible for generating the response to a request (comparable to
    the view layer in web frameworks).
    """

    async def handle(self, selector: str) -> Union[str, bytes, Menu]:
        """
        Receives a selector as a string, and returns the response as either a
        a string (for text responses), bytes (for binary responses), or a
        :class:`Menu <gopher_server.menu.Menu>` object.
        """
        pass


@implementer(IHandler)
class DirectoryHandler:
    """
    Serves files from a directory, as specified by `base_path`.

    .. note:: If the selector matches the name of a directory, this will look
              for a file called `index` in that directory.
    """

    def __init__(self, base_path: str):
        self.base_path = os.path.abspath(base_path)

    async def handle(self, selector: str) -> Union[str, bytes, Menu]:
        # Remove leading slash because os.path.join regards it as a full path
        # otherwise.
        if selector.startswith("/"):
            selector = selector[1:]

        file_path = os.path.abspath(os.path.join(self.base_path, selector))

        # Don't allow breaking out of the base directory.
        if not file_path.startswith(self.base_path):
            raise NotFound

        # TODO directory listing
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, "index")

        if not os.path.isfile(file_path):
            raise NotFound

        # TODO read binary files as bytes
        with open(file_path) as f:
            return f.read()


@implementer(IHandler)
class PatternHandler:
    """
    Uses pattern matching to map selectors to view functions.

    View functions can be registered by decorating them with the
    :func:`register <PatternHandler.register>` method. Requests with a selector
    matching the pattern will then call that function. For example:

    .. code-block::

       @handler.register("hello/.+")
       def hello(selector):
           return "hello %s" % selector[6:]

    Named capturing groups will be passed to the function as keyword
    arguments:

    .. code-block::

       @handler.register("hello/(?P<name>.+)")
       def hello(selector, name):
           return "hello %s" % name

    .. note:: Patterns are compared in the order in which they were
              registered, so if the selector matches multiple patterns then
              the one which was registered first will 'win'.
    """

    def __init__(self):
        self.patterns = []

    async def handle(self, selector: str) -> Union[str, bytes, Menu]:
        for pattern, func in self.patterns:
            match = pattern.match(selector)
            if match:
                return func(selector, **match.groupdict())
        raise NotFound

    def register(self, pattern: str):
        """Decorator to register a view function."""

        pattern = re.compile("^%s$" % pattern)

        def f(func):
            self.patterns.append((pattern, func))
            return func

        return f
