#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_inlierPrec_bench.py
#  Author: Alex Butenko, Georgia Institute of Technology
#  Creation Date: 06-01-2019
#  Last Modified: Sat Jun 1 00:03:28 2019
#
#  Description:test inlier benchmarks for geometric verification
#
#  Copyright (C) 2018 Alex Butenko
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
import bench.inlierPrecisionBench
import verifiers.ransac
import verifiers.learnedCoores
import verifiers.lmeds
import verifiers.mlesac
import dset.verification_dataset


if __name__ == "__main__":

    # Define epiConstraintBench benchmark
    inlierPrecisionBench = bench.inlierPrecisionBench.inlierPrecisionBench()

    # Define feature
    # ransac = verifiers.ransac.RANSAC()
    # lmeds = verifiers.lmeds.LMEDS()
    # lc = verifiers.learnedCoores.learnedCoores()
    mlesac = verifiers.mlesac.MLESAC()

    # Define dataset
    dataset = dset.verification_dataset.verification_dataset(['reichstag'])

    # Do the evaluation
    rep_result_r = inlierPrecisionBench.evaluate(
        dataset, mlesac, use_cache=False, save_result=True)

    rep_result = [rep_result_r]
    # Show the result
    for result_term in rep_result[0]['result_term_list']:
        bench.Utils.print_result(rep_result, result_term)
        bench.Utils.save_result(rep_result, result_term)

    #Show result for different sequences
    for sequence in dataset.sequences:
        for result_term in rep_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(rep_result, sequence, result_term)
            bench.Utils.save_sequence_result(rep_result, sequence, result_term)
