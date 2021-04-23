from typing import Callable, Dict, Any


class Interruptible:
    def __init__(self):
        self.__handlers: Dict[str, Callable] = {}

    def add_handler(self, name: str, handler: Callable):
        """
        Add interruption handler
        :param name Name of handler
        :param handler: Interruption handler
        """
        self.__handlers.update({name: handler})

    def __interrupt(self, name: str, data: Any):
        """
        Interrupts with named handler
        :param name: Name of handler
        :param data: Data that will be sent to handler
        """
        self.__handlers[name](data)
