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
import bench.epiConstraintBench
import verifiers.ransac
import verifiers.mlesac
import verifiers.learnedCorres
import verifiers.lmeds
import dset.verification_dataset


if __name__ == "__main__":

    # Define epiConstraintBench benchmark
    epiBench = bench.epiConstraintBench.epiConstraintBench()

    # Define feature
    ransac = verifiers.ransac.RANSAC()
    lmeds = verifiers.lmeds.LMEDS()
    learned = verifiers.learnedCorres.learnedCorres()
    ml = verifiers.mlesac.MLESAC()

    # Define dataset
    dataset = dset.verification_dataset.verification_dataset(['reichstag'])

    # Do the evaluation
    rep_result_r = epiBench.evaluate(
        dataset, ransac, use_cache=False, save_result=True)

    rep_result_l = epiBench.evaluate(
        dataset, lmeds, use_cache=False, save_result=True)

    rep_result_lr = epiBench.evaluate(
        dataset, learned, use_cache=False, save_result=True)

    rep_result_m = epiBench.evaluate(
        dataset, ml, use_cache=False, save_result=True)

    rep_result = [rep_result_r, rep_result_l, rep_result_m, rep_result_lr]

    # Show the result
    for result_term in rep_result[0]['result_term_list']:
        bench.Utils.print_result(rep_result, result_term)
        bench.Utils.save_result(rep_result, result_term)

    #Show result for different sequences
    # for sequence in vggh.sequence_name_list:
    #     for result_term in rep_result[0]['result_term_list']:
    #         bench.Utils.print_sequence_result(rep_result, sequence, result_term)
    #         bench.Utils.save_sequence_result(rep_result, sequence, result_term)
