import logging


class Callback(object):
    def __init__(self):
        self.log = logging.getLogger("root")
    """Start image processing pipeline."""
    def startProcessing(self, data) -> dict:
        """Overrides run jobs"""
        pass
