from dataclasses import dataclass

from gopher_server.handlers import IHandler, NotFound


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
            response = self.handler.handle(decoded_selector)
        except NotFound:
            return b"3Not found.\t\terror.host\t0\r\n.\r\n"
        except Exception:
            return b"3Internal server error.\t\terror.host\t0\r\n.\r\n"

        if isinstance(response, str):
            return response.encode("utf-8") + b"\r\n.\r\n"
        return response
