class Publisher:
    def __init__(self):
        self.callbacks = []

    def add_callback(self, callback):
        """
        Subscribe to publisher events, ask him to run callback
        :param callback: callback function
        """
        self.callbacks.append(callback)

    def broadcast(self, message):
        """
        Runs listeners callbacks
        :param message:
        """
        for callback in self.callbacks:
            callback(message)  # TODO: Run callback at new thread
