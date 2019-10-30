from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import PatternHandler
from gopher_server.listeners import tcp_listener, tcp_tls_listener, quic_listener
from gopher_server.menu import Menu, MenuItem, InfoMenuItem


handler = PatternHandler()


@handler.register("")
def home(request):
    return Menu([
        InfoMenuItem("hello world example menu"),
        MenuItem("0", "foo", "hello/foo", request.hostname, request.port),
        MenuItem("0", "bar", "hello/bar", request.hostname, request.port),
        MenuItem("0", "baz", "hello/baz", request.hostname, request.port),
    ])


@handler.register("hello/(?P<name>.+)")
def page(request, name):
    return "hello %s" % name


application = Application(handler)


if __name__ == "__main__":

    loop = get_event_loop()
    loop.create_task(tcp_listener(application, "localhost", "0.0.0.0", 7000))
    loop.create_task(tcp_tls_listener(
        application, "localhost", "0.0.0.0", 7001,
        "server.crt", "key.pem",
    ))
    loop.create_task(quic_listener(
        application, "localhost", "0.0.0.0", 7000,
        "server.crt", "key.pem",
    ))
    loop.run_forever()
