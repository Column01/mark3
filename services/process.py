import collections
import logging
from asyncio import SubprocessProtocol, transports

from events.server import ServerStart
from plugins.plugin import Plugin


class ProcessProtocol(SubprocessProtocol):
    """ Process Protocol that handles server process I/O """
    def __init__(self, exit_future):
        # Exit callback
        self.exit_future = exit_future
        # Scrollback buffer
        self.scrollback_buffer = collections.deque(maxlen=1000)

    def connection_made(self, transport: transports.BaseTransport):
        print("Connection with process established")
        self.transport = transport

    def pipe_data_received(self, fd: int, data: bytes):
        # Decode the data from the process and store it
        message = data.decode()
        self.scrollback_buffer.append(message)
        print(f"Data received: {message}")

    def process_exited(self):
        self.exit_future.set_result(True)

    def write_process(self, data: bytes):
        self.transport.write(data)


class Process(Plugin):
    """ The plugin that starts the server process """
    async def setup(self):
        self.register(ServerStart, self, self.start_server)
    
    async def start_server(self, event: ServerStart):
        logging.info(f"SERVER START EVENT FROM EVENT LOOP! Server name from event: {event.server_name}")
        self.loop.close()
