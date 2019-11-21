from argparse import ArgumentParser
from asyncio import get_event_loop

from gopher_server.application import Application
from gopher_server.handlers import DirectoryHandler
from gopher_server.listeners import tcp_listener


parser = ArgumentParser("gopher_server")
parser.add_argument("base_path", nargs="?", default=".")
args = parser.parse_args()


handler = DirectoryHandler(args.base_path)
application = Application(handler)


loop = get_event_loop()
loop.create_task(tcp_listener(application, "localhost", "0.0.0.0", 7000))
print("Serving on 0.0.0.0 port 7000...")
loop.run_forever()
