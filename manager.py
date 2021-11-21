import asyncio
import logging

from events.event import EventRegistry
from events.server import ServerStart
from services.process import Process


class Manager:
    """ The manager class that handles starting services, plugins and servers """
    def __init__(self, shared_path: str, server_name: str, server_path: str, sock_path: str, log_path: str):
        self.shared_path = shared_path
        self.server_name = server_name
        self.server_path = server_path

        # UNIX socket path
        self.sock_path = sock_path
        # Log path
        self.log_path = log_path

        self.event_registry = None
    
    async def start(self):
        """ Initializes services plugins and then starts the server """
        logging.info("Starting the manager")
        # Create the event registry object
        self.event_registry = EventRegistry()

        self.loop = asyncio.get_event_loop()

        # Start the process service
        process = Process(self.event_registry, self.loop)
        await process.setup()
        """ REGISTER OTHER SERVICES AND PLUGINS HERE """
        
        logging.info("Triggering the start event")
        # Trigger the server start in the process service
        await self.event_registry.dispatch(ServerStart(self.server_name))
