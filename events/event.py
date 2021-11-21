import logging
from typing import TYPE_CHECKING, Coroutine, Type

if TYPE_CHECKING:
    from plugins.plugin import Plugin


class Event:
    """ Base Event Class """
    async def cancel(self):
        """ Cancels the event """
        self.cancelled = True
    
    async def is_cancelled(self):
        """ Gets if the event was cancelled """
        return self.cancelled


class EventRegistry:
    """ Event Registry Class, used for registering and dispatching all events """
    def __init__(self):
        self.event_listeners = {}

    def register(self, event: Type[Event], plugin: "Plugin", callback: Coroutine):
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
        self.event_listeners[event_name].append((plugin, callback))

    def unregister(self, event: Type[Event], plugin: "Plugin", callback: Coroutine):
        """Un-registers the coroutine for handling the event

        Args:
            event (EventClass): The class of event for the listener you want to unregister
            plugin (Plugin): An instance of the plugin that was handling it
            callback (Coroutine): The coroutine that used to handle the event
        """
        event_name = event.__name__
        logging.info(f"Un-registering {event_name} handler for plugin: {plugin.__class__.__name__}")
        if self.event_listeners.get(event_name) is not None:
            self.event_listeners[event_name].remove((plugin, callback))

    async def dispatch(self, event: Event):
        """Dispatches an event

        Args:
            event (Event): An instance of the event you want to dispatch
        """
        event_name = type(event).__name__
        logging.info(f"Dispatching event: {event_name}")
        # Copy the event listeners to avoid mutation
        _event_listeners = self.event_listeners.copy()
        # Get all listeners for that event
        listeners = _event_listeners.get(event_name)
        if listeners is not None:
            # Dispatch the event to the callback
            for _, callback in listeners:
                await callback(event)
                # If the callback cancels the event, stop dispatching
                if await event.is_cancelled():
                    break
