from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import PatternHandler
from gopher_server.listeners import tcp_listener, quic_listener


handler = PatternHandler()


@handler.register("")
def home(selector):
    return "\r\n".join([
        "ihello world example menu\t\terror.host\t0",
        "0foo\thello/foo\tlocalhost\t7000",
        "0bar\thello/bar\tlocalhost\t7000",
        "0baz\thello/baz\tlocalhost\t7000",
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
