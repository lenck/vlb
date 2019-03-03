#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_ms_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Mar  2 12:47:41 2019
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
import dset.vgg_dataset


if __name__ == "__main__":

    vggh = dset.vgg_dataset.vggh_Dataset()
    vlsift_py = features.cyvlsift_official.cyvlsift_official()
    vlsift_load_matlab = features.vlsift_load_matlab.vlsift_load_matlab()
    ms_bench = bench.MatchingScoreBench.MatchingScoreBench()

    ms_result_py = ms_bench.evaluate(
        vggh, vlsift_py, use_cache=True, save_result=True)

    ms_result_matlab = ms_bench.evaluate(
        vggh, vlsift_load_matlab, use_cache=True, save_result=True)

    ms_result = [ms_result_py, ms_result_matlab]
    for result_term in ms_result[0]['result_term_list']:
        bench.Utils.print_result(ms_result, result_term)
        #Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        if sequence != 'graf':
            continue
        for result_term in ms_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(ms_result, sequence, result_term)
            bench.Utils.save_sequence_result(ms_result, sequence, result_term)
