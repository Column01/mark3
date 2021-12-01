import asyncio
import collections
import logging
import typing
from asyncio import SubprocessProtocol, transports

from events.event import EventFilter, EventPriority
from events.server import (ServerOutput, ServerStart, ServerStarting,
                           ServerStopped)
from plugins.plugin import Plugin

if typing.TYPE_CHECKING:
    from events.event import EventRegistry


class ProcessProtocol(SubprocessProtocol):
    """ Process Protocol that handles server process I/O """
    def __init__(self, exit_future: typing.Coroutine, event_registry: "EventRegistry"):
        # Exit future
        self.exit_future = exit_future

        # Reference to the event registry
        self.event_registry = event_registry
        # Running event loop
        self.loop = self.event_registry.loop

        self.scrollback_buffer = collections.deque(maxlen=1000)

    def connection_made(self, transport: transports.BaseTransport):
        logging.info("Connection with process established")
        self.transport = transport

        self.stdin = self.transport.get_pipe_transport(0)
        self.stdout = self.transport.get_pipe_transport(1)
        self.stderr = self.transport.get_pipe_transport(2)
        logging.info("Saved references to STDIN/OUT/ERR")

    def pipe_data_received(self, fd: int, data: bytes):
        # Decode the data from the process and store it
        message = data.decode().strip()

        # Check if the output was on the server STDOUT
        if fd == 1:
            # Dispatch the server output event to the event bus
            self.event_registry.dispatch_synchronous(ServerOutput(message))

    def process_exited(self):
        code = self.transport.get_returncode()
        self.loop.create_task(self.exit_future(code))

    async def write_process(self, data: typing.Union[bytes, str]):
        """Writes data to the STDIN of the process

        Args:
            data (typing.Union[bytes, str]): The bytes or string to send to the process
        """
        if isinstance(data, str):
            data = data.encode()
        self.stdin.write(data)


class Process(Plugin):
    """ The plugin that starts the server process """
    async def setup(self):
        self.register(ServerStart, self, self.start_server, EventPriority.MONITOR)
        self.register(ServerOutput, self, self.server_output, EventPriority.MONITOR)
        self.register(ServerStopped, self, self.server_stopped, EventPriority.MONITOR)

    async def start_server(self, event: ServerStart):
        logging.info(f"SERVER START EVENT FROM EVENT LOOP! Server name from event: {event.server_name}")

        # Build the process protocol
        self.protocol = ProcessProtocol(self.proc_closed, self.event_registry)

        # TODO: Gather info to build java command and arguments for server
        # Start server process and connect our custom protocol to it
        self._transport, self._protocol = await self.loop.subprocess_exec(
            lambda: self.protocol, 
            "python3",
            "test.py", 
            stdin=asyncio.subprocess.PIPE, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )

        await self.event_registry.dispatch(ServerStarting())
        # TODO: Console output tracking to wait until the server is fully started and then send a `ServerStarted` event

    async def server_output(self, event: ServerOutput):
        line = event.line
        logging.info(f"Line from server STDOUT: {line}")
        await self.protocol.write_process("say test")

    async def server_stopped(self, event: ServerStopped):
        logging.info(f"Server closed with reason: {event.reason}")

    async def proc_closed(self, exit_code):
        await self.event_registry.dispatch(ServerStopped(f"Process exited with code: {exit_code}"))
        logging.info("PROC CLOSED!")
        self.loop.stop()
