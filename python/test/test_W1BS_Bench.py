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
import features.np_sift
import dset.W1BS_dataset


if __name__ == "__main__":
    
    # Define baseline benchmark
    bench = bench.W1BSBench.W1BSBench()
    
    # Define feature
    np_sift_py = features.np_sift.np_sift()

    # Define dataset
    w1bs = dset.W1BS_dataset.W1BS_Dataset()
    
    # Do the evaluation
    result_py = bench.evaluate(w1bs, np_sift_py, use_cache=True, save_result=True)

    # Make the results from different detectors as a list. 
    result_list = [result_py]

    # Show the result
    bench.Utils.print_result(result_list, 'ap')
