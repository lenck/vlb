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
import math
from bench.VerificationBenchmarkTemplate import VerificationBenchmark

import bench.geom as geom

class inlierPrecisionBench(VerificationBenchmark):
    """
    EpiConstraint Template
    Return repeatability score and number of correspondence
    """
    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        super(inlierPrecisionBench, self).__init__(name='InlierPrecision', result_dir=result_dir)
        self.bench_name = 'inlierPrec'
        self.test_name = 'inlierPrec'

    def evaluate_unit(self, data_dict):
        """
        Single evaluation unit. Given two sets of points and an estimated Fundamental matrix
        return the Epipolar-Constraint Errors

        :param pts1: points to run from img1
        :type pts1: array
        :param pts2: points to run from img2
        :type pts2: array
        :param task: What to run
        :type task: dict

        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """
        est_F = data_dict['est_F']
        pts1 = data_dict['px_coords1']
        pts2 = data_dict['px_coords1']

        if est_F is None:
            est_F = geom.get_F_matrix_from_E(data_dict['est_E'],
                                             data_dict['K1'],
                                             data_dict['K2'])


        true_inliers = data_dict['inlier_mask']
        inlier_pts1, _, inlier_mask  = geom.get_inliers_F(pts1, pts2, est_F)

        prec, recall = self.get_pr_recall(true_inliers=true_inliers, est_inliers=inlier_mask)

        num_inliers = len(inlier_pts1)
        inlierPerc = float(num_inliers)/len(pts1)

        return num_inliers, inlierPerc, prec, recall

    def evaluate(self, dataset, verifier, use_cache=True,
                 save_result=True):
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

        result = self.evaluate_warpper(dataset, verifier, ['num_inliers', 'inlierPrec', 'precision','recall'],
                                       use_cache=use_cache, save_result=save_result)

        result['bench_name'] = self.bench_name
        return result

    def get_pr_recall(self, true_inliers, est_inliers):

        tp = np.sum(np.logical_and(true_inliers, est_inliers))
        fp = np.sum(np.logical_and(true_inliers==0, est_inliers==1))
        fn = np.sum(np.logical_and(true_inliers==1, est_inliers==0))
        tn = np.sum(np.logical_and(true_inliers==0, est_inliers==0))

        pr = tp/(tp+fp)
        recall = tp/(tp+fn)

        if math.isnan(pr):
            pr = 0.0
        if math.isnan(recall):
            recall = 0.0
        return pr, recall
