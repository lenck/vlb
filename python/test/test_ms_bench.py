#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_ms_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sun Mar  3 18:09:44 2019
#
#  Usage: python test_ms_bench.py
#  Description:test matching score benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

import os
import sys
cwd = os.getcwd()
sys.path.insert(0, '{}/python/'.format(cwd))

import bench.Utils
import bench.MatchingScoreBench
import bench.repBench
import features.cyvlsift_official
import features.vlsift_load_matlab
import features.cv_orb
import features.cv_mser
import features.cv_brisk
import features.cv_fast
import features.cv_akaze
import features.cv_kaze
import features.superpoint
import dset.vgg_dataset


if __name__ == "__main__":

    # Define matching score benchmark
    ms_bench = bench.MatchingScoreBench.MatchingScoreBench()

    # Define features
    vlsift_py = features.cyvlsift_official.cyvlsift_official()
    cv_orb = features.cv_orb.cv_orb()
    cv_brisk = features.cv_brisk.cv_brisk()
    cv_fast = features.cv_fast.cv_fast()
    cv_akaze = features.cv_akaze.cv_akaze()
    cv_kaze = features.cv_kaze.cv_kaze()
    superpoint = features.superpoint.SuperPoint()

    # Define dataset
    vggh = dset.vgg_dataset.vggh_Dataset()

    # Do the evaluation
    ms_result_vlsift = ms_bench.evaluate(
        vggh, vlsift_py, use_cache=True, save_result=True)

    ms_result_cv_orb = ms_bench.evaluate(
        vggh, cv_orb, use_cache=True, save_result=True)

    ms_result_cv_brisk = ms_bench.evaluate(
        vggh, cv_brisk, use_cache=True, save_result=True)

    ms_result_cv_kaze = ms_bench.evaluate(
        vggh, cv_kaze, use_cache=True, save_result=True)

    ms_result_cv_akaze = ms_bench.evaluate(
        vggh, cv_akaze, use_cache=True, save_result=True)

    ms_result_superpoint = ms_bench.evaluate(
        vggh, superpoint, use_cache=True, save_result=True)

    # Make the results from different detectors as a list.
    ms_result = [ms_result_vlsift, ms_result_cv_orb,
                 ms_result_cv_brisk, ms_result_cv_kaze,
                 ms_result_cv_akaze, ms_result_superpoint]

    # Show the result
    for result_term in ms_result[0]['result_term_list']:
        bench.Utils.print_result(ms_result, result_term)
        bench.Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(ms_result, sequence, result_term)
            bench.Utils.save_sequence_result(ms_result, sequence, result_term)
