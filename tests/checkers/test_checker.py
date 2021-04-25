import time


class Performance:
    @staticmethod
    def check(function) -> float:
        start = time.time()
        function()
        end = time.time() - start
        return end


class Accuracy:
    @staticmethod
    def check(function):
        pass
