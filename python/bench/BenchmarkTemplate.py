import matlab.engine
from abc import ABCMeta, abstractmethod

class Benchmark():
    __metaclass__ = ABCMeta 
    
    def __init__(self, name, tmp_feature_dir = './data/features/', result_dir = './python_scores/'):
        self.name = name
        self.tmp_feature_dir = tmp_feature_dir
        self.result_dir = result_dir


    @abstractmethod
    def evaluate(self, dataset, detector):
        pass
