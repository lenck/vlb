#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: BenchmarkTemplate.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sun Mar  3 16:36:17 2019
#
#  Description: Standard benchmark template
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

"""
This module describe benchmark template. 
A benchmark is given a detector/descriptor and a dataset, the way of performing the evluation.
"""

import numpy as np
from abc import ABCMeta, abstractmethod
import os
from tqdm import tqdm
import pickle as pkl

class Benchmark():
    __metaclass__ = ABCMeta
    
    """Benchmark Template
    
    Attributes
    ----------

    name: str
        Name of the dataset
    tmp_feature_dir: str
        Directory for saving the feature
    result_dir: str
        Directory for saving the final result
    """

    def __init__(self, name, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        self.name = name
        self.tmp_feature_dir = tmp_feature_dir
        self.result_dir = result_dir

    def detect_feature(self, dataset, detector,
                       use_cache=True, save_feature=True):
        """
        Extract feature from image.
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature 
        :rtype: dict
        """

        feature_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir,
                                          dataset.name, detector.name))
        except BaseException:
            pass

        pbar = tqdm(dataset)
        for sequence in pbar:
            pbar.set_description(
                "Extract feature for {} in {} with {}".format(
                    sequence.name, dataset.name, detector.name))
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset.name,
                                                                 detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name + '.npy')
                        get_feature_flag = True
                    except BaseException:
                        get_feature_flag = False

                if not get_feature_flag:
                    if detector.csv_flag:
                        feature_csv_name = './data/{}/{}/{}/{}-{}.frames.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                     detector.name, sequence.name, image.idx)
                        feature = self.load_csv_feature(feature_csv_name)
                        # pdb.set_trace()
                    else:
                        feature = detector.detect_feature(image.image_data)
                    # print(feature.shape)
                    if save_feature:
                        np.save(feature_file_name, feature)
                feature_dict['{}_{}'.format(
                    sequence.name, image.idx)] = feature

        return feature_dict

    def extract_descriptor(self, dataset, detector,
                           use_cache=False, save_feature=True):
        """
        Extract feature from image.
        
        :param dataset: Dataset to extract the descriptor
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature, descriptor 
        :rtype: dict, dict
        """
        feature_dict = {}
        descriptor_dict = {}

        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir,
                                          dataset.name, detector.name))
        except BaseException:
            pass

        pbar = tqdm(dataset)
        for sequence in pbar:
            pbar.set_description(
                "Extract feature for {} in {} with {}".format(
                    sequence.name, dataset.name, detector.name))
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir,
                                                                 dataset.name, detector.name, sequence.name, image.idx)
                descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir,
                                                                         dataset.name, detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name + '.npy')
                        descriptor = np.load(descriptor_file_name + '.npy')
                        get_feature_flag = True
                    except BaseException:
                        get_feature_flag = False

                if not get_feature_flag:
                    if detector.csv_flag:
                        feature_csv_name = './data/{}/{}/{}/{}-{}.frames.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                     detector.name, sequence.name, image.idx)
                        feature = self.load_csv_feature(feature_csv_name)
                        descriptor_csv_name = './data/{}/{}/{}/{}-{}.descs.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                       detector.name, sequence.name, image.idx)
                        descriptor = self.load_csv_feature(descriptor_csv_name)
                    else:
                        if detector.is_both:
                            feature, descriptor = detector.extract_all(
                                image.image_data)
                        else:
                            feature = detector.detect_feature(image.image_data)
                            descriptor = detector.extract_descriptor(
                                image.image_data, feature=feature)
                    if save_feature:
                        np.save(feature_file_name, feature)
                        np.save(descriptor_file_name, descriptor)

                feature_dict['{}_{}'.format(
                    sequence.name, image.idx)] = feature
                descriptor_dict['{}_{}'.format(
                    sequence.name, image.idx)] = descriptor

        return feature_dict, descriptor_dict

    def load_csv_feature(self, csv_feature_file):
        """
        Load feature from csvfile.
        
        :param csv_feature_file: csv file to load feature
        :type csv_feature_file: str
        :returns: feature
        :rtype: array
        """
        feature = []
        with open(csv_feature_file) as f:
            for line in f:
                tmp_list = line.split(';')
                float_list = [float(i) for i in tmp_list]
                feature.append(float_list)
        return np.asarray(feature)

    def load_feature(self, dataset_name, sequence_name, image, detector):
        """
        Load feature from cached file. If failed, extract feature from image
        
        :param dataset_name: Name of the dataset
        :type dataset_name: str
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :param image: Image
        :type image: Image
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :returns: feature
        :rtype: array
        """

        feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset_name,
                                                         detector.name, sequence_name, image.idx)
        try:
            feature = np.load(feature_file_name)
        except BaseException:
            feature = detector.detect_feature(image.image_data)
            np.save(feature_file_name, feature)

        return feature

    def load_descriptor(self, dataset_name, sequence_name, image, detector):
        """
        Load descriptor from cached file. If failed, extract descriptor from image
        
        :param dataset_name: Name of the dataset
        :type dataset_name: str
        :param sequence_name: Name of the sequence
        :type sequence_name: str
        :param image: Image
        :type image: Image
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :returns: descriptor
        :rtype: array
        """

        descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir, dataset_name,
                                                                 detector.name, sequence_name, image.idx)
        try:
            descriptor = np.load(descriptor_file_name)
        except BaseException:
            feature = detector.detect_feature(image.image_data)
            descriptor = detector.extract_descriptor(
                image.image_data, feature=feature)
            np.save(descriptor_file_name, descriptor)

        return descriptor

    # Evaluation warpper
    def evaluate_warpper(self, dataset, detector, result_list, extract_descriptor=False,
                         use_cache=True, save_result=True, custom_extraction=False):
        """
        Load descriptor from cached file. If failed, extract descriptor from image.

        **Structure of the result:**

        result['dataset_name']: name of the dataset

        result['result_term_list']: list of metrics for evaluation

        result['task_name']: name of the task

        result['detector_name']: name of the dataset

        result['sequence_result']: a list for result from each sequence

        result['ave_{}']: average value for each metric over all sequences


        **Structure of the sequence result:**

        sequence_result['sequence_name']: name of the  sequence

        sequence_result[result_name]: list of list of metrics over each link

        sequence_result['result_label_list']: label of each link in sequence_result (Same order)

        sequence_result['result_link_id_list']: ID of each link in sequence_result (Same order)


        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param result_list: Metric to calculate
        :type result_list: list
        :param extract_descriptor: Extract descriptor or not
        :type extract_descriptor: boolean
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        :param custom_extraction: Use custom extraction method or not. See also  and extract_descriptor_custom
        :type custom_extraction: boolean
        :returns: result 
        :rtype: dict

        See Also
        --------

        detect_feature_custom: Extract feature with customized method (special evaluation).
        extract_descriptor_custom: Extract descriptor with customized (special evaluation).

        """

        if custom_extraction:
            if extract_descriptor:
                feature_dict, descriptor_dict = self.extract_descriptor_custom(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)
            else:
                feature_dict = self.detect_feature_custom(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)

        else:
            if extract_descriptor:
                feature_dict, descriptor_dict = self.extract_descriptor(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)
            else:
                feature_dict = self.detect_feature(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)

        try:
            os.stat('{}{}/{}/{}/'.format(self.result_dir,
                                         self.bench_name, dataset.name, detector.name))
        except BaseException:
            os.makedirs('{}{}/{}/{}/'.format(self.result_dir,
                                             self.bench_name, dataset.name, detector.name))

        get_result_flag = False
        result_file_name = '{}{}/{}/{}/{}.pkl'.format(
            self.result_dir, self.bench_name, dataset.name, detector.name, self.test_name)
        if use_cache:
            try:
                result = pkl.load(open(result_file_name, 'rb'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except BaseException:
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

            # work with each sequence
            pbar = tqdm(dataset)
            for sequence in pbar:
                pbar.set_description(
                    "Processing {} in {} for {}".format(
                        sequence.name, dataset.name, detector.name))
                sequence_result = {}
                sequence_result['sequence_name'] = sequence.name
                for result_name in result_list:
                    sequence_result[result_name] = []
                sequence_result['result_label_list'] = []
                sequence_result['result_link_id_list'] = []

                try:
                    result['label'] = sequence.label
                except BaseException:
                    pass

                # for each link
                for link in sequence.links():
                    link = link[1]
                    try:
                        task = link.task
                    except BaseException:
                        task = None

                    feature_1 = feature_dict['{}_{}'.format(
                        sequence.name, link.source)]
                    feature_2 = feature_dict['{}_{}'.format(
                        sequence.name, link.target)]

                    if extract_descriptor:
                        descriptor_1 = descriptor_dict['{}_{}'.format(
                            sequence.name, link.source)]
                        descriptor_2 = descriptor_dict['{}_{}'.format(
                            sequence.name, link.target)]

                    sequence_result['result_link_id_list'].append(
                        "{}_{}".format(link.source, link.target))
                    sequence_result['result_label_list'].append(
                        dataset.get_image(sequence.name, link.target))
                    # for debug
                    #print("{}: {}_{}".format(sequence.name, link.source, link.target))
                    # if sequence.name == 'wall' and link.source=='1' and link.target == '2':
                    #    pdb.set_trace()
                    # simple evaluation function for each test

                    if extract_descriptor:
                        result_number_list = self.evaluate_unit(
                            (feature_1, descriptor_1), (feature_2, descriptor_2), task)
                    else:
                        result_number_list = self.evaluate_unit(
                            feature_1, feature_2, task)

                    for result_name, result_number in zip(
                            result_list, result_number_list):
                        # for debug
                        #print('{}: {}'.format(result_name, result_number))
                        sequence_result[result_name].append(result_number)

                for result_name in result_list:
                    sequence_result['ave_{}'.format(result_name)] = np.mean(
                        np.array(sequence_result['{}'.format(result_name)]))
                    result['ave_{}'.format(result_name)] = result['ave_{}'.format(
                        result_name)] + sequence_result['ave_{}'.format(result_name)]

                result['sequence_result'].append(sequence_result)
            # get average result
            for result_name in result_list:
                result['ave_{}'.format(result_name)] = result['ave_{}'.format(
                    result_name)] / len(result['sequence_result'])
                # for debug
                #print('ave {} {}'.format(result_name,result['ave_{}'.format(result_name)]))

            if save_result:
                with open(result_file_name, "wb") as output_file:
                    pkl.dump(result, output_file)

        return result

    def print_and_save_result(self, results):
        """
        Print and save result.

        :param results: Result to show
        :type results: dict
        """
        self.print_result(results)
        self.save_result(results)

    @abstractmethod
    def evaluate(self, dataset, detector):
        """
        Main function to run the evaluation wrapper. It could be different for different evaluation
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor

        See Also
        --------

        evaluate_warpper:
        """
        pass

    @abstractmethod
    def evaluate_unit(self, feature_1, feature_2, task):
        """
        Single evaluation unit. Given two features, return the result. Different for different benchmark
        
        :param feature_1: Feature to run. It can be feature or descriptor.
        :type feature_1: array 
        :param feature_2: Feature to run. It can be feature or descriptor.
        :type feature_2: array
        :param task: What to run
        :type task: dict
        
        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """
        pass

    @abstractmethod
    def detect_feature_custom(self, dataset, detector,
                              use_cache=False, save_feature=True):
        """
        Customized feature extraction method. For special task. 
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature 
        :rtype: dict

        See Also
        --------

        evaluate_warpper:
        extract_descriptor_custom:
        """
        pass

    @abstractmethod
    def extract_descriptor_custom(
            self, dataset, detector, use_cache=False, save_feature=True):
        """
        Customized description extraction method. For special task. 
        
        :param dataset: Dataset to extract the descriptor
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature 
        :rtype: dict

        See Also
        --------

        evaluate_warpper:
        extract_feature_custom:
        """
        pass
