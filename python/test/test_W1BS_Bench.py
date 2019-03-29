#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_W1BS_Bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sun Mar  3 22:43:21 2019
#
#  Usage: python test_W1BS_Bench.py
#  Description: Test baseline matching benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

import sys
import os

cwd = os.getcwd()
sys.path.insert(0, '{}/python/'.format(cwd))

import bench.Utils
import bench.W1BSBench
import features.cyvlsift_official
import features.cv_orb
import features.cv_mser
import features.cv_brisk
import features.cv_fast
import features.cv_akaze
import features.cv_kaze
import features.superpoint
import dset.W1BS_dataset


if __name__ == "__main__":

    # Define baseline benchmark
    w1bs_bench = bench.W1BSBench.W1BSBench()

    # Define feature
    vlsift_py = features.cyvlsift_official.cyvlsift_official()
    cv_orb = features.cv_orb.cv_orb()
    cv_brisk = features.cv_brisk.cv_brisk()
    cv_fast = features.cv_fast.cv_fast()
    cv_akaze = features.cv_akaze.cv_akaze()
    cv_kaze = features.cv_kaze.cv_kaze()
    superpoint = features.superpoint.SuperPoint()

    # Define dataset
    w1bs = dset.W1BS_dataset.W1BS_Dataset()

    # Do the evaluation
    result_vlsift = w1bs_bench.evaluate(
        w1bs, vlsift_py, use_cache=True, save_result=True)

    result_cv_orb = w1bs_bench.evaluate(
        w1bs, cv_orb, use_cache=True, save_result=True)

    result_cv_brisk = w1bs_bench.evaluate(
        w1bs, cv_brisk, use_cache=True, save_result=True)

    result_cv_kaze = w1bs_bench.evaluate(
        w1bs, cv_kaze, use_cache=True, save_result=True)

    result_cv_akaze = w1bs_bench.evaluate(
        w1bs, cv_akaze, use_cache=True, save_result=True)

    result_superpoint = w1bs_bench.evaluate(
        w1bs, superpoint, use_cache=True, save_result=True)

    # Make the results from different detectors as a list.
    result_list = [result_vlsift,result_cv_orb,result_cv_brisk,result_cv_kaze,result_cv_akaze,result_superpoint]

    # Show the result
    bench.Utils.print_result(result_list, 'ap')
