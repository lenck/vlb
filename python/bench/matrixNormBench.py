#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: matrixNormBench.py
#  Author: Alex Butenko, Georiga Institute of Technology
#  Creation Date: 06-01-2019
#  Last Modified: Sat Jun 1 21:46:25 2019
#
#  Description: Frobenius Norm Difference benchmark
#
#  Copyright (C) 2019 Alex Butenko
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================


"""
This module describe benchmark for Frobenius norm Difference.
"""

import numpy as np
import math
from bench.VerificationBenchmarkTemplate import VerificationBenchmark

import bench.geom as geom

class matrixNormBench(VerificationBenchmark):
    """
    EpiConstraint Template
    Return repeatability score and number of correspondence
    """
    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        super(matrixNormBench, self).__init__(name='InlierPrecision', result_dir=result_dir)
        self.bench_name = 'diffFrobenius '
        self.test_name = 'diffFrobenius'

    def evaluate_unit(self, data_dict):
        """
        Single evaluation unit. Given and estimated F matrix, find the Frobenius norm
        of the the difference from the true F

        :param data_dict: dictionary containing necessary data
        :type data_dict: dict

        """
        est_F = data_dict['est_F']
        true_F = data_dict['F']

        # Calculate F Matrix from E
        if est_F is None:
            est_F = geom.get_F_matrix_from_E(data_dict['est_E'],
                                             data_dict['K1'],
                                             data_dict['K2'])

        frobNorm = np.linalg.norm(true_F - est_F)

        return frobNorm

    def evaluate(self, dataset, verifier, use_cache=True,
                 save_result=True):
        """
        Main function to call the evaluation wrapper. It could be different for different evaluation

        :param dataset: Dataset to compare
        :type dataset: verification_dataset
        :param verifier: Verifier used to verify
        :type verifier: VerifierTemplate
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        :returns: result
        :rtype: dict
        """
        result = self.evaluate_warpper(dataset, verifier, ['diffFrobenius'],
                                       use_cache=use_cache, save_result=save_result)

        result['bench_name'] = self.bench_name
        return result
