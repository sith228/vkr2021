from typing import Callable, Dict, Any


class Interruptible:
    def __init__(self):
        self.__handlers: Dict[str, Callable] = {}

    def add_handler(self, name: str, handler: Callable):
        """
        Add interruption handler
        :param name Name of handler
        :param handler: Interruption handler
        :return none
        """
        self.__handlers.update({name: handler})

    def interrupt(self, name: str, data: Any):
        """
        Interrupts with named handler
        :param name: Name of handler
        :param data: Data that will be sent to handler
        :return none
        """
        self.__handlers[name](data)