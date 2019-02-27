#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_rep_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Fri Feb 15 14:59:00 2019
#
#  Usage: python test_rep_bench.py
#  Description:test repeatability benchmark
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
import repBench
import vlsift
import vgg_dataset


if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_py = vlsift.vlsift()
    rep_bench = repBench.repBench()

    rep_result_py = rep_bench.evaluate(
        vggh, vlsift_py, use_cache=False, save_result=True)

    rep_result = [rep_result_py]
    for result_term in rep_result[0]['result_term_list']:
        Utils.print_result(rep_result, result_term)
        Utils.save_result(rep_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in rep_result[0]['result_term_list']:
            Utils.print_sequence_result(rep_result, sequence, result_term)
            Utils.save_sequence_result(rep_result, sequence, result_term)
