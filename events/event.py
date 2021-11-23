import enum
import logging
from asyncio.events import AbstractEventLoop
from typing import TYPE_CHECKING, Coroutine, Type

if TYPE_CHECKING:
    from plugins.plugin import Plugin


class EventPriority(enum.Enum):
    """ The event priority used for dispatching events, lower number == higher priority """
    MONITOR = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    def __eq__(self, other):
        """ Check if we are equal to the other priority """
        return self.value == other.value if self.__class__ is other.__class__ else False

    def __lt__(self, other):
        """ Check if we are lesser than the other """
        return self.value < other.value if self.__class__ is other.__class__ else False
    
    def __gt__(self, other):
        """ Check if we are greater than the other """
        return self.value > other.value if self.__class__ is other.__class__ else False


class Event:
    """ Base Event Class """
    def __init__(self):
        self.cancelled = False

    async def cancel(self):
        """ Cancels the event """
        self.cancelled = True

    async def is_cancelled(self):
        """ Gets if the event was cancelled """
        return self.cancelled


class EventRegistry:
    """ Event Registry Class, used for registering and dispatching all events """
    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.event_listeners = {}

    def register(self, event: Type[Event], plugin: "Plugin", callback: Coroutine, priority: EventPriority):
        """Register a coroutine to handle an event

        Args:
            event (EventClass): The class of event you want to handle
            plugin (Plugin): An instance of the plugin that's handling it
            callback (Coroutine): The coroutine that will be used to handle the event
        """
        event_name = event.__name__
        logging.info(f"Registering {event_name} handler for plugin: {plugin.__class__.__name__}")
        if self.event_listeners.get(event_name) is None:
            self.event_listeners[event_name] = []
        self.event_listeners[event_name].append((priority, plugin, callback))

    def unregister(self, event: Type[Event], plugin: "Plugin", callback: Coroutine, priority: EventPriority):
        """Un-registers the coroutine for handling the event

        Args:
            event (EventClass): The class of event for the listener you want to unregister
            plugin (Plugin): An instance of the plugin that was handling it
            callback (Coroutine): The coroutine that used to handle the event
        """
        event_name = event.__name__
        logging.info(f"Un-registering {event_name} handler for plugin: {plugin.__class__.__name__}")
        if self.event_listeners.get(event_name) is not None:
            self.event_listeners[event_name].remove((priority, plugin, callback))

    async def dispatch(self, event: Event):
        """Dispatches an event

        Args:
            event (Event): An instance of the event you want to dispatch
        """
        event_name = type(event).__name__
        logging.info(f"Dispatching event: {event_name}")
        # Copy the event listeners to avoid errors if an event gets registered while we are iterating
        _event_listeners = self.event_listeners.copy()
        # Get all listeners for that event sorted by priority
        listeners = sorted(_event_listeners.get(event_name) or [], key=lambda y: y[0])

        if len(listeners) > 0:
            # Dispatch the event to the callback
            for _, _, callback in listeners:
                await callback(event)
                # If the callback cancels the event, stop dispatching
                if await event.is_cancelled():
                    break

    def dispatch_synchronous(self, event: Event):
        """Dispatches an event from synchronous code

        Args:
            event (Event): An instance of the event you want to dispatch
        """
        self.loop.create_task(self.dispatch(event))
