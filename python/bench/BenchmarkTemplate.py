from matlab.engine
from abc import ABCMeta, abstractmethod

class Benchmark():
    __metaclass__ = ABCMeta 

    eng = matlab.engine()
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def evaluate(self, dataset, detector):
        pass
