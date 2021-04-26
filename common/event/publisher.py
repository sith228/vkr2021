from . import Message


class Publisher:
    def __init__(self):
        self.__callbacks = []

    def add_callback(self, callback):
        """
        Subscribe to publisher events, ask him to run callback
        :param callback: callback function
        """
        self.__callbacks.append(callback)

    def __broadcast(self, message: Message):
        """
        Runs listeners callbacks
        :param message:
        """
        for callback in self.__callbacks:
            callback(message)  # TODO: Run callback at new thread
