"""
The module is the basic interface for benchmark

It contains basic wrapper function.

Author: Xu Zhang

"""
import matlab
import matlab.engine
import csv
import numpy as np
from abc import ABCMeta, abstractmethod
import os
from tqdm import tqdm
import hickle as hkl

#import pdb

eng = matlab.engine.start_matlab()
eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)

class Benchmark():
    __metaclass__ = ABCMeta 
    
    def __init__(self, name, tmp_feature_dir = './data/features/', result_dir = './python_scores/'):
        self.name = name
        self.tmp_feature_dir = tmp_feature_dir
        self.result_dir = result_dir
    
    def detect_feature(self, dataset, detector, use_cache = False, save_feature = True):
        feature_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir, dataset.name, detector.name))
        except:
            pass

        pbar = tqdm(dataset)
        for sequence in pbar:
            pbar.set_description("Extract feature for {} in {} with {}".format(sequence.name, dataset.name, detector.name))
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
                    if detector.csv_flag:
                        feature_csv_name = './data/{}/{}/{}/{}-{}.frames.csv'.format(self.tmp_feature_dir, dataset.name,\
                            detector.name, sequence.name, image.idx)
                        feature = self.load_csv_feature(feature_csv_name)
                        #pdb.set_trace()
                    else:
                        feature = detector.detect_feature(image.image_data)
                    #print(feature.shape)
                    if save_feature:
                        np.save(feature_file_name,feature)
                feature_dict['{}_{}'.format(sequence.name,image.idx)] = feature
                
        return feature_dict

    def extract_descriptor(self, dataset, detector, use_cache = False, save_feature = True):
        feature_dict = {}
        descriptor_dict = {}
        
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir, dataset.name, detector.name))
        except:
            pass
        
        pbar = tqdm(dataset)
        for sequence in pbar:
            pbar.set_description("Extract feature for {} in {} with {}".format(sequence.name, dataset.name, detector.name))
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir,\
                        dataset.name, detector.name, sequence.name, image.idx)
                descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir,\
                        dataset.name, detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name+'.npy')
                        descriptor = np.load(descriptor_file_name+'.npy')
                        get_feature_flag = True
                    except:
                        get_feature_flag = False
                        
                if not get_feature_flag:
                    if detector.csv_flag:
                        feature_csv_name = './data/{}/{}/{}/{}-{}.frames.csv'.format(self.tmp_feature_dir, dataset.name,\
                            detector.name, sequence.name, image.idx)
                        feature = self.load_csv_feature(feature_csv_name)
                        descriptor_csv_name = './data/{}/{}/{}/{}-{}.descs.csv'.format(self.tmp_feature_dir, dataset.name,\
                            detector.name, sequence.name, image.idx)
                        descriptor = self.load_csv_feature(descriptor_csv_name)
                    else:
                        if detector.is_both:
                            feature, descriptor = detector.extract_all(image.image_data)
                        else:
                            feature = detector.detect_feature(image.image_data)
                            descriptor = detector.extract_descriptor(image.image_data, feature = feature)
                    if save_feature:
                        np.save(feature_file_name,feature)
                        np.save(descriptor_file_name,descriptor)
                #print(feature.shape)
                #print(descriptor.shape)
                feature_dict['{}_{}'.format(sequence.name,image.idx)] = feature
                descriptor_dict['{}_{}'.format(sequence.name,image.idx)] = descriptor
         
        return feature_dict, descriptor_dict

    def load_csv_feature(self,csv_feature_file):
        feature = []
        with open(csv_feature_file) as f:
            for line in f:
                tmp_list = line.split(';')
                float_list = [float(i) for i in tmp_list]
                feature.append(float_list)
        return np.asarray(feature)
    
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
    
    #Evaluation warpper
    def evaluate_warpper(self, dataset, detector, result_list, extract_descriptor = False,
            use_cache = True, save_result = True):
         
        if extract_descriptor:
            feature_dict, descriptor_dict = self.extract_descriptor(dataset, detector, use_cache = use_cache, save_feature = save_result)
        else:
            feature_dict = self.detect_feature(dataset,detector, use_cache = use_cache, save_feature = save_result)

        try:
            os.makedirs('{}{}/{}/{}/'.format(self.result_dir, self.bench_name, dataset.name, detector.name))
        except:
            pass
        
        get_result_flag = False
        result_file_name = '{}{}/{}/{}/{}.hkl'.format(self.result_dir, self.bench_name, dataset.name, detector.name, self.test_name)
        if use_cache:
            try:
                result = hkl.load(open(result_file_name,'r'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except:
                get_result_flag = False

        if not get_result_flag:
            result = {}
            result['dataset_name'] = dataset.name
            result['result_term_list'] = result_list
            result['task_name'] = self.name
            result['detector_name'] = detector.name
            result['sequence_result'] = []
            for result_name in result_list:
                result['ave_{}'.format(result_name)] = 0.0
            
            #work with each sequence
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

                #for each link
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
                    #for debug
                    #print("{}: {}_{}".format(sequence.name, link.source, link.target))
                    #if sequence.name == 'wall' and link.source=='1' and link.target == '2':
                    #    pdb.set_trace()
                    #simple evaluation function for each test
                    if extract_descriptor:
                        result_number_list = self.evaluate_unit((feature_1,descriptor_1), (feature_2,descriptor_2), task)
                    else:
                        result_number_list = self.evaluate_unit(feature_1, feature_2, task)
                    
                    for result_name, result_number in zip(result_list, result_number_list):
                        #for debug
                        #print('{}: {}'.format(result_name, result_number))
                        sequence_result[result_name].append(result_number)

                for result_name in result_list:
                    sequence_result['ave_{}'.format(result_name)] = np.mean(np.array(sequence_result['{}'.format(result_name)]))
                    result['ave_{}'.format(result_name)] = result['ave_{}'.format(result_name)]+sequence_result['ave_{}'.format(result_name)]

                result['sequence_result'].append(sequence_result)
            # get average result
            for result_name in result_list: 
                result['ave_{}'.format(result_name)] = result['ave_{}'.format(result_name)]/len(result['sequence_result'])
                #for debug
                #print('ave {} {}'.format(result_name,result['ave_{}'.format(result_name)]))

            if save_result:
                with open(result_file_name, "w") as output_file:
                    hkl.dump(result, output_file)

        return result

    def print_and_save_result(results):
        self.print_result(results)
        self.save_result(results)

    @abstractmethod
    def evaluate(self, dataset, detector):
        pass

    @abstractmethod
    def evaluate_unit(feature_1, feature_2, task):
        pass
