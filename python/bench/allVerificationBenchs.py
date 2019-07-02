#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: allVerificationBench.py
#  Author: Alex Butenko, Georgia Institute of Technology
#  Creation Date: 06-01-2019
#  Last Modified: Sat Jun 1 21:46:25 2019
#
#  Description: All verifcation Benchmarks
#
#  Copyright (C) 2019 Alex Butenko
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


class allVerificationBenchs(VerificationBenchmark):
    """
    Benchmark used to run all Verification Benchmarks:

    Benchmarks Tested
    -----------------
    - Mean Epipolar Distance
    - Median Epipolar Distance
    - Number of Inliers
    - Inlier Percentage
    - Precision
    - Recall
    - Absolute Epipolar Constraint
    - Squared Epipolar Constraint
    - Frobenius Norm of Difference from GT Fundamental matrix
    """
    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        super(allVerificationBenchs, self).__init__(name='Epipolar Distance', result_dir=result_dir)
        self.bench_name = 'allVerificationBenchs'
        self.test_name = 'allVerificationBenchs'

    def evaluate_unit(self, data_dict):
        """
        Single evaluation unit. Given a dictionary of correspondence informatino between
        an image pair, run each verification on the image pair

        :param data_dict: Dictionary of data for an image pair.
        :type data_dict: dict

        **Structure of the data_dict:**
        data_dict['norm_coords1']: List of normalized coordinates for
                                    img1 of correspondence pair

        data_dict['norm_coords2']: List of normalized coordinates for
                                    img2 of correspondence pair

        data_dict['px_coords1']: List of pixel coordinates for
                                    img1 of correspondence pair

        data_dict['px_coords2']: List of pixel coordinates for
                                    img2 of correspondence pair

        data_dict['K1']:  3x3 np.array; Camera calibration matrix of cam from img1

        data_dict['K2']:  3x3 np.array; Camera calibration matrix of cam from img2

        data_dict['E']:  3x3 np.array; Ground-truth Essential Matrix from img1 to img2

        data_dict['F']:  3x3 np.array; Ground-truth Fundamental Matrix from img1 to img2

        data_dict['inlier_mask']: Nx1 np.array; Binary array indicating true correspondences

        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """
        est_F = data_dict['est_F']
        true_F = data_dict['F']
        pts1 = data_dict['px_coords1']
        pts2 = data_dict['px_coords1']

        if est_F is None:
            est_F = geom.get_F_matrix_from_E(data_dict['est_E'],
                                             data_dict['K1'],
                                             data_dict['K2'])

        #Run Processes

        #Get Inliers from estimated Fundamental Matrix
        inlier_pts1, inlier_pts2, inlier_mask  = geom.get_inliers_F(pts1, pts2, est_F, dist_type='symmetric')

        #Epipolar Distance
        epiDists = geom.get_epidist(pts1, pts2, est_F, type='symmetric')

        #Frobenius Norm Distance
        frobNorm = np.linalg.norm(true_F - est_F)

        #MEAN-D and MEDIAN-D
        mean_d = np.mean(epiDists)
        median_d = np.median(epiDists)

        #Precision and Recall
        true_inliers = data_dict['inlier_mask']
        prec, recall = geom.get_pr_recall(true_inliers=true_inliers, est_inliers=inlier_mask)

        #Inlier Percentage
        num_inliers = len(inlier_pts1)
        inlierPerc = float(num_inliers)/len(pts1)

        #Epipolar Constraint Metric
        epiConst = geom.get_epi_constraint(inlier_pts1, inlier_pts2, est_F)
        epiAbs = np.sum(np.abs(epiConst))
        epiSqr = np.sum(epiConst**2)


        return mean_d, median_d, num_inliers, inlierPerc, prec, recall, epiAbs, epiSqr, frobNorm

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

        result = self.evaluate_warpper(dataset, verifier, [ 'mean_d', 'median_d', 'num_inliers',
                                                           'inlierPerc', 'precision', 'recall',
                                                           'epiAbs', 'epiSqr', 'Frobenius Norm'],
                                       use_cache=use_cache, save_result=save_result)

        result['bench_name'] = self.bench_name
        return result
