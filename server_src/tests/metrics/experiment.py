from typing import Dict, List


class Experiment:
    def __init__(self, name: str, model: str = None):
        """
        :param name: Name of experiment
        :param model: Type experiment model
        """
        self.name: str = name
        if model in [None, 'accuracy', 'performance']:
            self.model: str = model
        else:
            raise ValueError('Unknown model')
        self.values: Dict = {}

    def append(self, name: str, values: List):
        """
        Appends values to experiment
        :param name: Name of values block
        :param values: Values that should be appended
        :return: Nothing
        """
        self.values.update({name: values})
