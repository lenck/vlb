#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: W1BSBench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Mar  5 22:58:54 2019
#
#  Description:Wide baseline matching benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

"""
This module describe benchmark for baseline matching. 
"""

import numpy as np
import os
import bench.BenchmarkTemplate
from tqdm import tqdm
from bench.BenchmarkTemplate import Benchmark
import sys
import other_benchmarks.wxbs_descriptors_benchmark.code.utils.w1bs as w1bs


class W1BSBench(Benchmark):
    """
    Baseline matching benchmark
    Return ap 
    """
    def __init__(self, tmp_feature_dir='./features/',
                 result_dir='./python_scores/'):
        super(
            W1BSBench,
            self).__init__(
            name='Baseline Stereo',
            tmp_feature_dir=tmp_feature_dir,
            result_dir=result_dir)
        self.bench_name = 'descbm'
        self.test_name = 'baseline_stereo'

    def evaluate_unit(self, feature_1, feature_2, task):
        """
        Single evaluation unit. Given two features, return the repeatability.
        
        :param feature_1: Feature and descriptor to run.
        :type feature_1: list of array [feature, descriptor] 
        :param feature_2: Feature and descriptor to run. 
        :type feature_2: list of array [feature, descriptor]
        :param task: What to run
        :type task: dict
        
        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """
        _, descriptor_1 = feature_1
        _, descriptor_2 = feature_2
        match_dict, match_matrix = w1bs.match_descriptors(descriptor_1, descriptor_2,
                                                                metric="L2", batch_size=256)
        is_correct = (match_matrix[:, 0] ==
                      match_matrix[:, 1]).astype(np.float32)
        r, p, ap = w1bs.get_recall_and_pecision(match_matrix[:, 3], is_correct, n_pts=100,
                                                      smaller_is_better=True)
        return [ap]

    def evaluate(self, dataset, detector, use_cache=True, save_result=True):
        """
        Main function to call the evaluation wrapper. It could be different for different evaluation
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        :returns: result 
        :rtype: dict

        See Also
        --------
        
        bench.Benchmark
        bench.Benchmark.evaluate_warpper:
        """
        result = self.evaluate_warpper(dataset, detector, ['ap'], extract_descriptor=True,
                                       use_cache=use_cache, save_result=save_result, custom_extraction=True)
        return result

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

        """

        pass

    def extract_descriptor_custom(
            self, dataset, detector, use_cache=False, save_feature=True):
        """
        Customized description extraction method. Get descriptor from images of patches. 
        
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
                descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir,
                                                                         dataset.name, detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        descriptor = np.load(descriptor_file_name + '.npy')
                        get_feature_flag = True
                    except BaseException:
                        get_feature_flag = False

                if not get_feature_flag:
                    if detector.csv_flag:
                        descriptor_csv_name = './data/{}/{}/{}/{}-{}.descs.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                       detector.name, sequence.name, image.idx)
                        descriptor = self.load_csv_feature(descriptor_csv_name)
                    else:
                        h, w = image.image_data.shape
                        n_patches = h // w
                        patches_set = np.zeros((n_patches, w, w, 1))
                        for i in range(n_patches):
                            patches_set[i, :, :, 0] = image.image_data[i *
                                                                       (w): (i + 1) * (w), 0:w]
                        descriptor = detector.extract_descriptor_from_patch(
                            patches_set)

                    if save_feature:
                        np.save(descriptor_file_name, descriptor)

                feature_dict['{}_{}'.format(sequence.name, image.idx)] = {}
                descriptor_dict['{}_{}'.format(
                    sequence.name, image.idx)] = descriptor

        return feature_dict, descriptor_dict
