from events.event import Event


class ServerStart(Event):
    """ Issued to start a server """
    def __init__(self, server_name: str):
        self.server_name = server_name
