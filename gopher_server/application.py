class Application:
    async def dispatch(self, selector: bytes) -> bytes:
        try:
            decoded_selector = selector.decode("utf-8")
        except UnicodeDecodeError:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        decoded_selector = decoded_selector.strip()

        if "\t" in decoded_selector or "\r" in decoded_selector or "\n" in decoded_selector:
            return b"3Bad selector.\t\terror.host\t0\r\n.\r\n"

        return b"iHello world!\t\terror.host\t0\r\n.\r\n"

