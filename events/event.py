from typing import Type, Callable

from services.service import Service


class Event:
    """ Base Event Class """
    async def cancel(self):
        self.cancelled = True
    
    async def is_cancelled(self):
        return self.cancelled

EventClass = Type(Event)
ServiceClass = Type(Service)

class EventRegistry:
    """ Event Registry Class, used for registering and dispatching all events """
    def __init__(self):
        self.event_listeners = {}

    async def register(self, event: EventClass, service: ServiceClass, callback: Callable):
        if self.event_listeners.get(event) is None:
            self.event_listeners[event] = []
        self.event_listeners[event].append((service, callback))

    async def unregister(self, event: EventClass, service: ServiceClass, callback: Callable):
        if self.event_listeners.get(event) is not None:
            self.event_listeners[event].remove((service, callback))

    async def dispatch(self, event: EventClass):
        # Get all listeners for that event
        listeners = self.event_listeners.get(event)
        if listeners is not None:
            # Dispatch the event to the callback
            for _, callback in listeners:
                await callback(event)
                if await event.is_cancelled():
                    break
