import enum
import logging
import re
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


class EventFilter:
    """ Used by when registering an event handler to filter for event contents """
    def __init__(self, pattern: str, event_field_name: str):
        """Creates the filter object for filtering an event

        Args:
            filters (List[Tuple[str, str]]): A list of tuples where the first tuple item is event field and the second is a regex pattern to match
        """
        self.pattern = pattern
        self.event_field_name = event_field_name

    def check(self, event: "Event"):
        """Checks the event against the stored filter to see if it should be dispatched to the listener

        Args:
            event (Event): The event instance to check against the filter

        Returns:
            match (bool): Whether the event should be dispatched to the listener
        """
        logging.info(f"Event field name: {self.event_field_name} Regex pattern: {self.pattern}")
        event_field = getattr(event, self.event_field_name)
        # Inline hack for easy bool from regex search
        match = re.search(self.pattern, event_field) is not None
        logging.info(f"Contents of event field: {event_field}. Match? {match}")

        return match


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

    def register(self, event: Type[Event], plugin: "Plugin", callback: Coroutine, priority: EventPriority, event_filter: EventFilter = None):
        """Register a coroutine to handle an event

        Args:
            event (EventClass): The class of event you want to handle
            plugin (Plugin): An instance of the plugin that's handling it
            callback (Coroutine): The coroutine that will be used to handle the event
            event_filter (EventFilter, optional): An instance of an event filter
        """
        event_name = event.__name__
        logging.info(f"Registering {event_name} handler for plugin: {plugin.__class__.__name__}")
        if self.event_listeners.get(event_name) is None:
            self.event_listeners[event_name] = []
        self.event_listeners[event_name].append((priority, plugin, callback, event_filter))

    def unregister(self, event: Type[Event], plugin: "Plugin", callback: Coroutine, priority: EventPriority, event_filter: EventFilter = None):
        """Un-registers the coroutine for handling the event

        Args:
            event (EventClass): The class of event for the listener you want to unregister
            plugin (Plugin): An instance of the plugin that was handling it
            callback (Coroutine): The coroutine that used to handle the event
            event_filter (EventFilter, optional): An instance of an event filter
        """
        event_name = event.__name__
        logging.info(f"Un-registering {event_name} handler for plugin: {plugin.__class__.__name__}")
        if self.event_listeners.get(event_name) is not None:
            self.event_listeners[event_name].remove((priority, plugin, callback, event_filter))

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
            for _, _, callback, event_filter in listeners:
                # Check if listener provided a filter and if so, check the filter
                if event_filter is None or event_filter.check(event):
                    # Trigger the callback
                    await callback(event)
                    # If the callback cancels the event, stop dispatching it
                    if await event.is_cancelled():
                        break

    def dispatch_synchronous(self, event: Event):
        """Dispatches an event from synchronous code

        Args:
            event (Event): An instance of the event you want to dispatch
        """
        self.loop.create_task(self.dispatch(event))
