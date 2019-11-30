import os.path
import re

try:
    import filetype
    FILETYPE_ENABLED = True
except ImportError:
    FILETYPE_ENABLED = False

from dataclasses import dataclass
from inspect import iscoroutinefunction
from logging import getLogger
from typing import Union
from zope.interface import Interface, implementer

from gopher_server.menu import Menu, MenuItem

log = getLogger(__name__)


@dataclass
class Request:
    hostname: str
    port:     int
    selector: str


class NotFound(Exception):
    pass


class IHandler(Interface):
    """
    Interface for handler classes.

    A handler is called by the :class:`Application <gopher_server.application.Application>`,
    and is responsible for generating the response to a request (comparable to
    the view layer in web frameworks).
    """

    async def handle(self, request: Request) -> Union[str, bytes, Menu]:
        """
        Receives a :class:`Request <gopher_server.handlers.Request>` object,
        and returns the response as either a string (for text responses), bytes
        (for binary responses), or a :class:`Menu <gopher_server.menu.Menu>`
        object. May also raise
        :class:`NotFound <gopher_server.handlers.NotFound>`.
        """
        pass


def _file_type(path):
    if os.path.isdir(path):
        return "1"
    if not FILETYPE_ENABLED:
        log.warn(
            "The filetype dependency is not installed. "
            "Defaulting to 0 (text)."
        )
        return "0" # text
    kind = filetype.guess(path)
    if kind is None:
        return "0" # text
    if kind.mime == "image/gif":
        return "g"
    if kind.mime.startswith("image/"):
        return "I"
    if kind.mime.startswith("audio/"):
        return "s"
    return "9" # binary


def _menu_from_directory(request, path):
    menu = Menu()

    for name in sorted(os.listdir(path)):
        file_type = _file_type(os.path.join(path, name))
        menu.append(MenuItem(
            file_type,
            name,
            os.path.join(request.selector, name),
            request.hostname,
            request.port,
        ))

    return menu


@implementer(IHandler)
class DirectoryHandler:
    """
    Serves files from a directory, as specified by `base_path`.

    If the selector matches the name of a directory, this will look for a file
    called `index` in that directory and serve that.

    Setting the `generate_menus` argument to `True` will instead serve an
    automatically generated menu listing all the files in the directory. This
    uses the `filetype` library for type detection, which you can install using
    the `automenu` extras::

        pip install gopher_server[automenu]

    If `filetype` is not installed then all file entries will have type `0`
    (text).

    """

    def __init__(self, base_path: str, generate_menus=False):
        self.base_path = os.path.abspath(base_path)
        self.generate_menus = generate_menus

    async def handle(self, request: Request) -> Union[str, bytes, Menu]:
        selector = request.selector

        # Remove leading slash because os.path.join regards it as a full path
        # otherwise.
        if selector.startswith("/"):
            selector = selector[1:]

        file_path = os.path.abspath(os.path.join(self.base_path, selector))

        # Don't allow breaking out of the base directory.
        if not file_path.startswith(self.base_path):
            raise NotFound

        if os.path.isdir(file_path):
            if self.generate_menus:
                return _menu_from_directory(request, file_path)
            else:
                file_path = os.path.join(file_path, "index")

        if not os.path.isfile(file_path):
            raise NotFound

        with open(file_path, "rb") as f:
            data = f.read()
            try:
                return data.decode("utf-8")
            except UnicodeDecodeError:
                return data


@implementer(IHandler)
class PatternHandler:
    """
    Uses regular expression matching to map selectors to view functions.

    View functions can be registered by decorating them with the
    :func:`register <PatternHandler.register>` method. Requests with a selector
    matching the regex pattern will then call that function. For example:

    .. code-block::

       @handler.register("hello/.+")
       def hello(request):
           return "hello %s" % request.selector[6:]

    Named capturing groups will be passed to the function as keyword
    arguments:

    .. code-block::

       @handler.register("hello/(?P<name>.+)")
       def hello(request, name):
           return "hello %s" % name

    .. note:: Patterns are compared in the order in which they were
              registered, so if the selector matches multiple patterns then
              the one which was registered first will "win".
    """

    def __init__(self):
        self.patterns = []

    async def handle(self, request: Request) -> Union[str, bytes, Menu]:
        for pattern, func in self.patterns:
            match = pattern.match(request.selector)
            if match:
                if iscoroutinefunction(func):
                    return await func(request, **match.groupdict())
                return func(request, **match.groupdict())
        raise NotFound

    def register(self, pattern: str):
        """Decorator to register a view function."""

        pattern = re.compile("^%s$" % pattern)

        def f(func):
            self.patterns.append((pattern, func))
            return func

        return f
