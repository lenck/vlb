#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: tests_epiDist_bench.py
#  Author: Alex Butenko, Georiga Institute of Technology
#  Creation Date: 06-01-2019
#  Last Modified: Sat Jun 1 21:46:25 2019
#
#  Description: Test epipolar distance benchmark
#
#  Copyright (C) 2019 Alex Butenko
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
import bench.epiDistanceBench
import verifiers.ransac
import verifiers.lmeds
import dset.verification_dataset


if __name__ == "__main__":

    # Define epiConstraintBench benchmark
    epiDistanceBench = bench.epiDistanceBench.epiDistanceBench()

    # Define feature
    ransac = verifiers.ransac.RANSAC()
    lmeds = verifiers.lmeds.LMEDS()

    # Define dataset
    dataset = dset.verification_dataset.verification_dataset()

    # Do the evaluation
    rep_result_r = epiDistanceBench.evaluate(
        dataset, ransac, use_cache=False, save_result=True)

    rep_result_l = epiDistanceBench.evaluate(
        dataset, lmeds, use_cache=False, save_result=True)

    rep_result = [rep_result_r, rep_result_l]

    # Show the result
    for result_term in rep_result[0]['result_term_list']:
        bench.Utils.print_result(rep_result, result_term)
        bench.Utils.save_result(rep_result, result_term)

    # TODO add show_sequence flag
    for sequence in dataset.sequence_name_list:
        for result_term in rep_result[0]['result_term_list']:
            bench.Utils.print_sequence_result(rep_result, sequence, result_term)
            bench.Utils.save_sequence_result(rep_result, sequence, result_term)
