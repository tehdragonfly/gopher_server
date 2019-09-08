from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import PatternHandler
from gopher_server.listeners import tcp_listener, quic_listener
from gopher_server.menu import Menu, MenuItem, InfoMenuItem


handler = PatternHandler()


@handler.register("")
def home(selector):
    return Menu([
        InfoMenuItem("hello world example menu"),
        MenuItem("0", "foo", "hello/foo", "localhost", 7000),
        MenuItem("0", "bar", "hello/bar", "localhost", 7000),
        MenuItem("0", "baz", "hello/baz", "localhost", 7000),
    ])


@handler.register("hello/(?P<name>.+)")
def page(selector, name):
    return "hello %s" % name


application = Application(handler)


if __name__ == "__main__":

    loop = get_event_loop()
    loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
    loop.create_task(quic_listener(
        application, "0.0.0.0", 7000,
        "server.crt", "key.pem",
    ))
    loop.run_forever()
