from dataclasses import dataclass
from logging import getLogger

from gopher_server.handlers import IHandler, NotFound, Request
from gopher_server.menu import Menu

log = getLogger(__name__)


@dataclass
class Application:
    """
    Core of the Gopher server application.

    This class is responsible for the basic semantics of the Gopher protocol,
    including decoding the selector line and encoding the response.

    .. note:: The bytes<->string conversion uses UTF-8, but the Gopher RFC
              specifies ASCII encoding. Some clients may have issues if you
              use characters outside the ASCII range.
    """

    handler: IHandler

    async def dispatch(self, hostname: str, port: int, selector: bytes) -> bytes:
        """
        Dispatches a request.

        This is called by a listener, and in turn calls the `Application`'s
        handler. The hostname and port are passed through in a
        :class:`Request <gopher_server.handlers.Request>` object so that
        handlers which generate a menu can include the right values for local
        selectors.
        """

        try:
            decoded_selector = selector.decode("utf-8")
        except UnicodeDecodeError:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        decoded_selector = decoded_selector.strip()

        if "\t" in decoded_selector or "\r" in decoded_selector or "\n" in decoded_selector:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        request = Request(hostname, port, decoded_selector)

        try:
            response = await self.handler.handle(request)
        except NotFound:
            return b"3Not found.\t\terror.host\t0\r\n.\r\n"
        except Exception as e:
            log.error("Caught exception:", exc_info=e)
            return b"3Internal server error.\t\terror.host\t0\r\n.\r\n"

        if isinstance(response, Menu):
            response = response.serialize()

        if isinstance(response, str):
            encoded_response = response.encode("utf-8")
            encoded_response = encoded_response.replace(b"\n", b"\r\n")
            if not encoded_response.endswith(b"\r\n"):
                encoded_response += b"\r\n"
            return encoded_response + b".\r\n"

        return response
