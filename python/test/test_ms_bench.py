#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_ms_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Mon Apr 15 14:57:08 2019
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
import pickle as pkl

from config import models_to_test

if __name__ == "__main__":

    # Define matching score benchmark
    ms_bench = bench.MatchingScoreBench.MatchingScoreBench(matchGeometry=False)

    # Define dataset
    vggh = dset.vgg_dataset.vggh_Dataset()

    ms_result = list()
    for (modelName, model) in models_to_test:
        vgg_result = ms_bench.evaluate(vggh, model, use_cache=True, save_result=True)
        ms_result.append(vgg_result)

    # ms_result = [ms_result_superpoint]

    with open('results.pkl', 'wb') as f:
        pkl.dump(ms_result, f)

    # Show the result
    for result_term in ms_result[0]['result_term_list']:
        bench.Utils.print_result(ms_result, result_term)
        bench.Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(ms_result, sequence, result_term)
            bench.Utils.save_sequence_result(ms_result, sequence, result_term)
