#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_W1BS_Bench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Feb  9 11:14:17 2019
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
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(
    0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')

import Utils
import W1BSBench
import np_sift
import W1BS_dataset


if __name__ == "__main__":

    w1bs = W1BS_dataset.W1BS_Dataset()
    np_sift = np_sift.np_sift()
    bench = W1BSBench.W1BSBench()

    result = bench.evaluate(w1bs, np_sift, use_cache=True, save_result=True)
    result = [result]
    Utils.print_result(result, 'ap')
