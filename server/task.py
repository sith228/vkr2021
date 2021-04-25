import numpy as np

from server.network.event import Event


class Task:
    def __init__(self, event: Event, image: np.ndarray = None):
        self.event = event
        self.image = image
