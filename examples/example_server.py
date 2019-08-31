from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import DirectoryHandler
from gopher_server.listeners import tcp_listener, quic_listener


if __name__ == "__main__":
    handler     = DirectoryHandler("data")
    application = Application(handler)

    loop = get_event_loop()
    loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
    loop.create_task(quic_listener(
        application, "0.0.0.0", 7002,
        "server.crt", "key.pem",
    ))
    loop.run_forever()
