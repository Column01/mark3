from typing import Coroutine, Type

from services.service import Service


class Event:
    """ Base Event Class """
    async def cancel(self):
        """ Cancels the event """
        self.cancelled = True
    
    async def is_cancelled(self):
        """ Gets if the event was cancelled """
        return self.cancelled

# Typing stuff
EventClass = Type(Event)
ServiceClass = Type(Service)


class EventRegistry:
    """ Event Registry Class, used for registering and dispatching all events """
    def __init__(self):
        self.event_listeners = {}

    def register(self, event: EventClass, service: ServiceClass, callback: Coroutine):
        """Register a coroutine to handle an event

        Args:
            event (EventClass): The event you want to handle
            service (ServiceClass): An instance of the plugin that's handling it
            callback (Coroutine): The coroutine that will be used to handle the event
        """
        if self.event_listeners.get(event) is None:
            self.event_listeners[event] = []
        self.event_listeners[event].append((service, callback))

    def unregister(self, event: EventClass, service: ServiceClass, callback: Coroutine):
        """Un-registers the coroutine for handling the event

        Args:
            event (EventClass): The event for the listener you want to unregister
            service (ServiceClass): An instance of the plugin that was handling it
            callback (Coroutine): The coroutine that used to handle the event
        """
        if self.event_listeners.get(event) is not None:
            self.event_listeners[event].remove((service, callback))

    async def dispatch(self, event: EventClass):
        """Dispatches an event

        Args:
            event (EventClass): An instance of the event you want to dispatch
        """
        # Copy the event listeners to avoid mutation
        _event_listeners = self.event_listeners.copy()
        # Get all listeners for that event
        listeners = _event_listeners.get(event)
        if listeners is not None:
            # Dispatch the event to the callback
            for _, callback in listeners:
                await callback(event)
                # If the callback cancels the event, stop dispatching
                if await event.is_cancelled():
                    break
