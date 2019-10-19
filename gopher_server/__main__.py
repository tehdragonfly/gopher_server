from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import DirectoryHandler
from gopher_server.listeners import tcp_listener


handler = DirectoryHandler(".")
application = Application(handler)


loop = get_event_loop()
loop.create_task(tcp_listener(application, "0.0.0.0", 7000))
print("Serving on 0.0.0.0 port 7000...")
loop.run_forever()
