#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: repBench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Mar  5 21:46:25 2019
#
#  Description:repeatability benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

"""
This module describe benchmark for repeatability.
"""

import numpy as np
import bench.BenchmarkTemplate
from bench.BenchmarkTemplate import Benchmark
import scipy.io as sio

from bench.ellipse_overlap_H import ellipse_overlap_H

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})
import bench.vlb_greedy_matching


class repBench(Benchmark):
    """
    Repeatability Template
    Return repeatability score and number of correspondence
    """
    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        super(repBench, self).__init__(name='Repeatability',
                                       tmp_feature_dir=tmp_feature_dir, result_dir=result_dir)
        self.bench_name = 'decrep'
        self.test_name = 'repeatability'

    def evaluate_unit(self, feature_1, feature_2, task):
        """
        Single evaluation unit. Given two features, return the repeatability.

        :param feature_1: Feature to run.
        :type feature_1: array
        :param feature_2: Feature to run.
        :type feature_2: array
        :param task: What to run
        :type task: dict

        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """

        rep = 0.0
        num_cor = 0
        if feature_1 is None or feature_2 is None or feature_1.shape[
                0] == 0 or feature_2.shape[0] == 0:
            rep = 0.0
            num_cor = 0
        else:
            option = {}
            option['maxOverlapError'] = 0.5
            geo_info = task
            tcorr, corr_score, info = ellipse_overlap_H(
                geo_info, feature_1, feature_2, option)

            if len(corr_score) == 0 or corr_score.size == 0:
                rep = 0.0
                num_cor = 0
            else:
                # have to use a stable sort method
                perm_index = np.argsort(1 - corr_score, kind='mergesort')
                tcorr_s = tcorr[perm_index, :]
                fa_valid = info['fa_valid']
                fb_valid = info['fb_valid']

                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
                matches, _ = bench.vlb_greedy_matching.vlb_greedy_matching(
                    fa_num, fb_num, tcorr_s)
                overlapped_num = np.sum(matches[:, 0] > -1)
                num_cor = overlapped_num

                if self.norm_factor == 'minab':
                    rep = overlapped_num / float(min(fa_num, fb_num))
                elif self.norm_factor == 'a':
                    rep = overlapped_num / float(fa_num)
                elif self.norm_factor == 'b':
                    rep = overlapped_num / float(fb_num)

        return rep, num_cor

    def evaluate(self, dataset, detector, use_cache=True,
                 save_result=True, norm_factor='minab'):
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
        :param norm_factor: How to normalize the repeatability. Option: minab, a, b
        :type norm_factor: str
        :returns: result
        :rtype: dict

        See Also
        --------

        bench.Benchmark
        bench.Benchmark.evaluate_warpper:
        """

        self.norm_factor = norm_factor
        result = self.evaluate_warpper(dataset, detector, ['repeatability', 'num_cor'], extract_descriptor=False,
                                       use_cache=use_cache, save_result=save_result)
        result['norm_factor'] = norm_factor
        result['bench_name'] = self.bench_name
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

        """

        pass
