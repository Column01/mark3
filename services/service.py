class Service:
    def __init__(self, instance):
        self.instance = instance

    def register(self):
        self.instance.register(self)
