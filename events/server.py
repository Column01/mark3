from typing import Union

from events.event import Event


class ServerStart(Event):
    """ Issued to start a server """
    def __init__(self, server_name: str, server_path: str):
        self.server_name = server_name
        self.server_path = server_path
        super().__init__()


class ServerStarting(Event):
    """ Issued when the server is starting up """
    def __init__(self):
        super().__init__()


class ServerStarted(Event):
    """ Issued with the server has started up """
    def __init__(self):
        super().__init__()


class ServerOutput(Event):
    """ Issued when the server process issues a line to STDOUT """
    def __init__(self, line: str):
        self.line = line
        super().__init__()


class ServerInput(Event):
    """ Issued to send data to the server process STDIN """
    def __init__(self, data: Union[str, bytes]):
        self.data = data
        super().__init__()


class ServerStop(Event):
    """ Issued to stop the server """
    def __init__(self):
        super().__init__()


class ServerStopping(Event):
    """ Issued while the server is stopping """
    def __init__(self):
        super().__init__()


class ServerStopped(Event):
    """ Issued when the server process stops """
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__()
