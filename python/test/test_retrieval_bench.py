#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_retrieval_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sun Mar  3 17:58:13 2019
#
#  Usage: python test_retrieval_bench.py
#  Description: Test retrieval benchmark
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

import bench.RetrievalBenchmark
import features.cyvlsift_official
import dset.oxford5k_dataset
import dset.paris6k_dataset
import bench.Utils

if __name__ == "__main__":

    # Define retrieval benchmark
    retrieval_bench = bench.RetrievalBenchmark.RetrievalBenchmark()

    # Define feature
    vlsift_py = features.cyvlsift_official.cyvlsift_official()
    
    # Define dataset
    paris6k = dset.paris6k_dataset.paris6k_Dataset()

    # Do the test
    map_result_py = retrieval_bench.evaluate(
        paris6k, vlsift_py, use_cache=True, save_result=True)

    # Make the results from different detectors as a list. 
    # (Only one here, but you can add more)
    map_result = [map_result_py]

    # Show the result
    for result_term in map_result[0]['result_term_list']:
        bench.Utils.print_retrieval_result(map_result, 'm' + result_term)
        bench.Utils.save_retrieval_result(map_result, 'm' + result_term)

    
    # Another dataset
    oxford5k = dset.oxford5k_dataset.oxford5k_Dataset()
    map_result_py = retrieval_bench.evaluate(
        oxford5k, vlsift_py, use_cache=True, save_result=True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        bench.Utils.print_retrieval_result(map_result, 'm' + result_term)
        bench.Utils.save_retrieval_result(map_result, 'm' + result_term)
