from events.event import Event


class ServerStart(Event):
    """ Issued to start a server """
    def __init__(self, server_name: str, server_path: str):
        self.server_name = server_name
        self.server_path = server_path
        super().__init__()
