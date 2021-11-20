from services.service import Service
from asyncio import SubprocessProtocol, transports

import collections


class ProcessProtocol(SubprocessProtocol):
    def __init__(self, exit_future):
        # Exit callback
        self.exit_future = exit_future
        # Scrollback buffer
        self.scrollback_buffer = collections.deque(maxlen=1000)

    def connection_made(self, transport: transports.BaseTransport) -> None:
        print("Connection with process established")
        self.transport = transport

    def pipe_data_received(self, fd: int, data: bytes) -> None:
        # Decode the data from the process and store it
        message = data.decode()
        self.scrollback_buffer.append(message)
        print(f"Data received: {message}")

    def process_exited(self):
        self.exit_future.set_result(True)

    def write_process(self, data: bytes):
        self.transport.write(data)


class Process(Service):
    """ The service to actually start the server process """
    def __init__(self):
        pass