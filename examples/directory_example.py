from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import DirectoryHandler
from gopher_server.listeners import tcp_listener, tcp_tls_listener, quic_listener


handler = DirectoryHandler("data")
application = Application(handler)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
    loop.create_task(tcp_tls_listener(
        application, "0.0.0.0", 7001,
        "server.crt", "key.pem",
    ))
    loop.create_task(quic_listener(
        application, "0.0.0.0", 7000,
        "server.crt", "key.pem",
    ))
    loop.run_forever()
