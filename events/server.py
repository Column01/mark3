from events.event import Event


class ServerStart(Event):
    """ Issued to start a server """
    def __init__(self, server_name: str, server_path: str):
        self.server_name = server_name
        self.server_path = server_path
        super().__init__()


class ServerOutput(Event):
    """ Issued when the server process issues a line to STDOUT """
    def __init__(self, line: str):
        self.line = line
        super().__init__()


class ServerStopped(Event):
    """ Issued when the server process stops """
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__()
