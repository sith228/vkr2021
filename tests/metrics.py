from typing import Any


class Metrics:
    @staticmethod
    def write(metric: str, value: Any):
        file = open("metrics.txt", "a")
        file.write(metric + " " + str(value) + "\n")
