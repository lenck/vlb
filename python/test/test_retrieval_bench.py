#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_retrieval_bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Feb 26 22:15:46 2019
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
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import Utils
import RetrievalBenchmark
import repBench
import cyvlsift_official
import oxford5k_dataset
import paris6k_dataset

if __name__ == "__main__":

    paris6k = paris6k_dataset.paris6k_Dataset()
    oxford5k = oxford5k_dataset.oxford5k_Dataset()
    vlsift_py = cyvlsift_official.cyvlsift_official()
    retrieval_bench = RetrievalBenchmark.RetrievalBenchmark()

    map_result_py = retrieval_bench.evaluate(
        paris6k, vlsift_py, use_cache=True, save_result=True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        Utils.print_retrieval_result(map_result, 'm' + result_term)
        Utils.save_retrieval_result(map_result, 'm' + result_term)

    map_result_py = retrieval_bench.evaluate(
        oxford5k, vlsift_py, use_cache=True, save_result=True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        Utils.print_retrieval_result(map_result, 'm' + result_term)
        Utils.save_retrieval_result(map_result, 'm' + result_term)
