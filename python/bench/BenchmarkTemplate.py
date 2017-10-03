"""
The module is the basic interface for benchmark

It contains basic input and output funtion and display function.

Author: Xu Zhang

"""

import matlab.engine
import csv
import numpy as np
from abc import ABCMeta, abstractmethod

from tqdm import tqdm
import hickle as hkl

eng = None
eng = matlab.engine.start_matlab()
eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)

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
   
    def detect_feature(self, dataset, detector, use_cache = False, save_feature = True):
        feature_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir, dataset.name, detector.name))
        except:
            pass

        for sequence in dataset:
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset.name,\
                        detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name+'.npy')
                        get_feature_flag = True
                    except:
                        get_feature_flag = False
                        
                if not get_feature_flag:
                    feature = detector.detect_feature(image.image_data)
                    print(feature.shape)
                    if save_feature:
                        np.save(feature_file_name,feature)
                feature_dict['{}_{}'.format(sequence.name,image.idx)] = feature
                
        return feature_dict

    def extract_descriptor(self, dataset, descriptor, use_cache = False, save_feature = True):
        feature_dict = {}
        descriptor_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir, dataset.name, detector.name))
        except:
            pass

        for sequence in dataset:
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset.name,\
                        detector.name, sequence.name, image.idx)
                descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir, dataset.name,\
                        detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name+'.npy')
                        descriptor = np.load(descriptor_file_name+'.npy')
                        get_feature_flag = True
                    except:
                        get_feature_flag = False
                        
                if not get_feature_flag:
                    if detector.is_both:
                        feature, descriptor = detector.extract_all(image.image_data)
                    else:
                        feature = detector.detect_feature(image.image_data)
                        descriptor = detector.extract_descriptor(image.image_data, feature = feature)
                    if save_feature:
                        np.save(feature_file_name,feature)
                        np.save(descriptor_file_name,descriptor)
                feature_dict['{}_{}'.format(sequence.name,image.idx)] = feature
                descriptor_dict['{}_{}'.format(sequence.name,image.idx)] = descriptor
                
        return feature_dict, descriptor_dict

    def load_feature(self, dataset_name, sequence_name, image, detector):
        feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset_name,\
                        detector.name, sequence_name, image.idx)
        try:
            feature = np.load(feature_file_name)
        except:
            feature = detector.detect_feature(image.image_data)
            np.save(feature_file_name,feature)

        return feature
    
    def load_descriptor(self, dataset_name, sequence_name, image, detector):
        descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir, dataset_name,\
                        detector.name, sequence_name, image.idx)
        try:
            descriptor = np.load(descriptor_file_name)
        except:
            feature = detector.detect_feature(image.image_data)
            descriptor = detector.extract_descriptor(image.image_data, feature = feature)
            np.save(descriptor_file_name,descriptor)

        return descriptor

    def evaluate_warpper(self, dataset, detector, result_list, extract_descriptor = False,
            use_cache = True, save_result = True):
        
        if extract_descriptor:
            feature_dict, descriptor_dict = self.detect_feature(dataset,detector, use_cache, save_result)
        else:
            feature_dict = self.detect_feature(dataset,detector, use_cache = True, save_feature = True)

        try:
            os.makedirs('{}detrep/{}/{}/'.format(self.result_dir, dataset.name, detector.name))
        except:
            pass

        get_result_flag = False
        result_file_name = '{}detrep/{}/{}/repeatability.hkl'.format(self.result_dir, dataset.name, detector.name)

        if use_cache:
            try:
                result = hkl.load(open(result_file_name,'r'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except:
                get_result_flag = False

        if not get_result_flag:
            #if BenchmarkTemplate.eng is None:
            #    BenchmarkTemplate.eng = matlab.engine.start_matlab()
            #    BenchmarkTemplate.eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)
            result = {}
            result['dataset_name'] = dataset.name
            result['task_name'] = self.name
            result['detector_name'] = detector.name
            result['sequence_result'] = []
            for result_name in result_list:
                result['ave_{}'.format(result_name)] = 0.0

            pbar = tqdm(dataset)
            for sequence in pbar:
                pbar.set_description("Processing {} in {} for {}".format(sequence.name, dataset.name, detector.name))
                sequence_result = {}
                sequence_result['sequence_name'] = sequence.name
                for result_name in result_list:
                    sequence_result[result_name] = []
                sequence_result['result_label_list'] = []
                sequence_result['result_link_id_list'] = []
                
                try:
                    result['label'] = sequence.label
                except:
                    pass

                for link in sequence.links():
                    link = link[1]
                    task = link.matlab_task
                    feature_1 = feature_dict['{}_{}'.format(sequence.name, link.source)]
                    feature_2 = feature_dict['{}_{}'.format(sequence.name, link.target)]
                    if extract_descriptor:
                        descriptor_1 = descriptor_dict['{}_{}'.format(sequence.name, link.source)]
                        descriptor_2 = descriptor_dict['{}_{}'.format(sequence.name, link.target)]

                    sequence_result['result_link_id_list'].append("{}_{}".format(link.source, link.target))
                    sequence_result['result_label_list'].append(dataset.get_image(sequence.name, link.target))
                    
                    if extract_descriptor:
                        result_number_list = self.evaluate_unit((feature_1,descriptor_1), (feature_2,descriptor_2), task)
                    else:
                        result_number_list = self.evaluate_unit(feature_1, feature_2, task)
                    
                    for result_name, result_number in zip(result_list, result_number_list):
                        sequence_result[result_name].append(result_number)

                for result_name in result_list:
                    sequence_result['ave_{}'.format(result_name)] = np.mean(np.array(sequence_result['{}'.format(result_name)]))
                    result['ave_{}'.format(result_name)] = result['ave_{}'.format(result_name)]+sequence_result['ave_{}'.format(result_name)]

                result['sequence_result'].append(sequence_result)

            for result_name in result_list: 
                result['ave_{}'.format(result_name)] = result['ave_{}'.format(result_name)]/len(result['sequence_result'])
                print('ave {} {}'.format(result_name,result['ave_{}'.format(result_name)]))

            if save_result:
                with open(result_file_name, "w") as output_file:
                    hkl.dump(result, output_file)

        return result

    @abstractmethod
    def evaluate_unit(feature_1, feature_2, task):
        pass

    @abstractmethod
    def print_result_sequence(result,results,sequence):
        pass

    @abstractmethod
    def print_result(self,results):
        pass

    @abstractmethod
    def save_result(self,results):
        pass
    
    def print_and_save_result(results):
        self.print_result(results)
        self.save_result(results)

    @abstractmethod
    def get_str_list(self,results):
        pass

    @abstractmethod
    def evaluate(self, dataset, detector):
        pass
