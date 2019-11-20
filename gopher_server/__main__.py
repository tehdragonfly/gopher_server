from asyncio import get_event_loop
from sys import argv

from gopher_server.application import Application
from gopher_server.handlers import DirectoryHandler
from gopher_server.listeners import tcp_listener


if len(argv) > 1:
    base_path = argv[1]
else:
    base_path = "."

handler = DirectoryHandler(base_path)
application = Application(handler)


loop = get_event_loop()
loop.create_task(tcp_listener(application, "localhost", "0.0.0.0", 7000))
print("Serving on 0.0.0.0 port 7000...")
loop.run_forever()
