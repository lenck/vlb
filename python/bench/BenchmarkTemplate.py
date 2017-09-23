import matlab.engine
import csv
from abc import ABCMeta, abstractmethod

eng = None
#eng = matlab.engine.start_matlab()
#eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)

class Benchmark():
    __metaclass__ = ABCMeta 
    
    def __init__(self, name, tmp_feature_dir = './data/features/', result_dir = './python_scores/'):
        self.name = name
        self.tmp_feature_dir = tmp_feature_dir
        self.result_dir = result_dir
    
    def print_table(self, content_list):
        if len(content_list)==0:
            return

        max_detector_name_len = 8
        max_sequence_name_len = 6

        for content in content_list:
            if len(content[0])>max_detector_name_len:
                max_detector_name_len = len(content[0])

        content = content_list[0][1:]
        for sequence_name in content:
            if len(sequence_name)>max_sequence_name_len:
                max_sequence_name_len = len(sequence_name)

        content = content_list[0]
        title_str = ''
        for idx, this_str in enumerate(content):
            if idx == 0:
                title_str = "|{}|".format(this_str.ljust(max_detector_name_len)[:max_detector_name_len])
            else:
                title_str = title_str+"{}|".format(this_str.ljust(max_sequence_name_len)[:max_sequence_name_len]) 
                
        print('-'*len(title_str))
        print(title_str)
        print('-'*len(title_str))
        content_str = ''
        for content in content_list[1:]:
            for idx, this_str in enumerate(content):
                if idx == 0:
                    content_str = "|{}|".format(this_str.ljust(max_detector_name_len)[:max_detector_name_len])
                else:
                    content_str = content_str + "{}|".format(this_str.ljust(max_sequence_name_len)[:max_sequence_name_len])
            print(content_str)

        print('-'*len(title_str))
        return
    
    @abstractmethod
    def print_result_sequence(result,results,sequence):
        pass

    @abstractmethod
    def print_result(self,results):
        pass

    @abstractmethod
    def save_result(self,results):
        pass

    @abstractmethod
    def get_str_list(self,results):
        pass

    @abstractmethod
    def print_and_save_result(results):
        pass

    @abstractmethod
    def evaluate(self, dataset, detector):
        pass
