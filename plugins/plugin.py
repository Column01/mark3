class Plugin:
    def __init__(self, event_registry):
        # Reference to the event registry
        self.event_registry = event_registry
        # Reference to register an event callback
        self.register = self.event_registry.register

        # Setup the event and it's callbacks
        self.setup()
    
    def setup(self):
        pass
