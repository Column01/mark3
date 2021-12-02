import typing


if typing.TYPE_CHECKING:
    from asyncio.events import AbstractEventLoop
    from events.event import EventRegistry


class Plugin:
    def __init__(self, event_registry: "EventRegistry", loop: "AbstractEventLoop"):
        # Reference to the event registry
        self.event_registry = event_registry
        # Reference to register an event callback
        self.register = self.event_registry.register
        self.unregister = self.event_registry.unregister

        # Reference to the event loop
        self.loop = loop
    
    async def setup(self):
        pass
