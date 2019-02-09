#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_ms_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Feb  9 11:11:30 2019
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
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import Utils
import MatchingScoreBench
import repBench
import vlsift
import vgg_dataset


if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_py = vlsift.vlsift()
    ms_bench = MatchingScoreBench.MatchingScoreBench()

    ms_result_py = ms_bench.evaluate(
        vggh, vlsift_py, use_cache=False, save_result=True)

    ms_result = [ms_result_py]
    for result_term in ms_result[0]['result_term_list']:
        Utils.print_result(ms_result, result_term)
        Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            Utils.print_sequence_result(ms_result, sequence, result_term)
            Utils.save_sequence_result(ms_result, sequence, result_term)
