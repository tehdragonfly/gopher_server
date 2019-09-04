from dataclasses import dataclass
from logging import getLogger

from gopher_server.handlers import IHandler, NotFound

log = getLogger(__name__)


@dataclass
class Application:
    handler: IHandler

    async def dispatch(self, selector: bytes) -> bytes:
        try:
            decoded_selector = selector.decode("utf-8")
        except UnicodeDecodeError:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        decoded_selector = decoded_selector.strip()

        if "\t" in decoded_selector or "\r" in decoded_selector or "\n" in decoded_selector:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        try:
            response = await self.handler.handle(decoded_selector)
        except NotFound:
            return b"3Not found.\t\terror.host\t0\r\n.\r\n"
        except Exception as e:
            log.error("Caught exception:", exc_info=e)
            return b"3Internal server error.\t\terror.host\t0\r\n.\r\n"

        if isinstance(response, str):
            encoded_response = response.encode("utf-8")
            encoded_response = encoded_response.replace(b"\n", b"\r\n")
            if not encoded_response.endswith(b"\r\n"):
                encoded_response += b"\r\n"
            return encoded_response + b".\r\n"

        return response
