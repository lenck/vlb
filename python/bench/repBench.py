import numpy as np
import json
import os
from BenchmarkTemplate import Benchmark
from abc import ABCMeta, abstractmethodr
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')


class repBench(Benchmark):
    def evaluate(self, dataset, detector):
        return feature
