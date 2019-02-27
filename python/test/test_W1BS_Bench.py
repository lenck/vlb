#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_W1BS_Bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Wed Feb 20 19:33:15 2019
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
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import Utils
import W1BSBench
import np_sift
#import cyvlsift_official
#import cyvlsift_official_old
#import vlsift_python
import W1BS_dataset


if __name__ == "__main__":

    w1bs = W1BS_dataset.W1BS_Dataset()
    #vlsift_py_old = cyvlsift_official_old.cyvlsift_official_old()
    #vlsift_py = cyvlsift_official.cyvlsift_official()
    #vlsift_python = vlsift_python.vlsift_python(peak_thresh = 0.005)
    np_sift_py = np_sift.np_sift()
    bench = W1BSBench.W1BSBench()

    result_py = bench.evaluate(w1bs, np_sift_py, use_cache=True, save_result=True)
    result_list = [result_py]
    Utils.print_result(result_list, 'ap')
