#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_rep_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Mar  5 00:03:28 2019
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
sys.path.insert(0, '{}/python/'.format(cwd))

import bench.Utils
import bench.repBench
import features.cyvlsift_official
import dset.vgg_dataset


if __name__ == "__main__":

    # Define repeatability benchmark
    rep_bench = bench.repBench.repBench()
    
    # Define feature 
    vlsift_py = features.cyvlsift_official.cyvlsift_official()

    # Define dataset
    vggh = dset.vgg_dataset.vggh_Dataset()

    # Do the evaluation
    rep_result_py = rep_bench.evaluate(
        vggh, vlsift_py, use_cache=True, save_result=True)

    # Make the results from different detectors as a list. 
    # (Only one here, but you can add more)
    rep_result = [rep_result_py]

    # Show the result
    for result_term in rep_result[0]['result_term_list']:
        bench.Utils.print_result(rep_result, result_term)
        bench.Utils.save_result(rep_result, result_term)

    #Show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in rep_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(rep_result, sequence, result_term)
            bench.Utils.save_sequence_result(rep_result, sequence, result_term)
