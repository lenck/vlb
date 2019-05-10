#!/usr/bin/python
#-*- coding: utf-8 -*-
#===========================================================
#  File Name: VerificationBenchmarkTemplate.py
#  Author: Alex Butenko, Georgia Institute of Technology
#  Creation Date: 05-08-2019
#  Last Modified: Wed May 08 21:45:20 2019
#
#  Description: Standard geometric verification benchmark template
#
#  Copyright (C) 2019 Alex Butenko
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

"""
This module describe a verification benchmark template.
A benchmark is given a verification algorithm and a dataset, the way of performing the evluation.
"""

import numpy as np
from abc import ABCMeta, abstractmethod
import os
from tqdm import tqdm
import pickle as pkl

class VerificationBenchmark():
    __metaclass__ = ABCMeta

    """Benchmark Template

    Attributes
    ----------

    name: str
        Name of the dataset
    tmp_feature_dir: str
        Directory for saving the feature
    result_dir: str
        Directory for saving the final result
    """

    def __init__(self, name,
                 result_dir='./python_scores/'):
        self.name = name
        self.result_dir = result_dir



    def find_F_matrix(self, verifier, data_dict):
        pts1 = data_dict['px_coords1']
        pts2 = data_dict['px_coords2']
        return verifier.estimate_fundamental_matrix(pts1, pts2)


    def find_E_matrix(self, verifier, data_dict):
        pts1 = data_dict['norm_coords1']
        pts2 = data_dict['norm_coords2']
        return verifier.estimate_essential_matrix(pts1, pts2)

    # Evaluation warpper
    def evaluate_warpper(self, dataset, verifier, result_list, use_cache=True, save_result=True):
        """
        Load descriptor from cached file. If failed, extract descriptor from image.

        **Structure of the result:**

        result['dataset_name']: name of the dataset

        result['result_term_list']: list of metrics for evaluation

        result['task_name']: name of the task

        result['name']: name of the verification algorithm

        result['sequence_result']: a list for result from each sequence

        result['ave_{}']: average value for each metric over all sequences


        **Structure of the sequence result:**

        sequence_result['sequence_name']: name of the  sequence

        sequence_result[result_name]: list of list of metrics over each link

        :param dataset: Dataset to extract the feature
        :type dataset: verification_dataset
        :param verifier: Verifier used for geometric verification
        :type verifier: Verification
        :param result_list: Metric to calculate
        :type result_list: list
        :param save_result: Save result or not
        :type save_result: boolean
        :returns: result
        :rtype: dict

        See Also
        --------
        """


        try:
            os.stat('{}{}/{}/{}/'.format(self.result_dir,
                                         self.bench_name, dataset.name, verifier.name))
        except BaseException:
            os.makedirs('{}{}/{}/{}/'.format(self.result_dir,
                                             self.bench_name, dataset.name, verifier.name))

        get_result_flag = False
        result_file_name = '{}{}/{}/{}/{}.pkl'.format(
            self.result_dir, self.bench_name, dataset.name, verifier.name, self.test_name)
        if use_cache:
            try:
                result = pkl.load(open(result_file_name, 'rb'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except BaseException:
                get_result_flag = False

        if not get_result_flag:
            result = {}
            result['dataset_name'] = dataset.name
            result['result_term_list'] = result_list
            result['task_name'] = self.name
            result['detector_name'] = verifier.name
            result['sequence_result'] = []
            for result_name in result_list:
                result['ave_{}'.format(result_name)] = 0.0

            # work with each sequence
            data = dataset.get_data()
            pbar = tqdm(data)
            for sequence in pbar:
                pbar.set_description(
                    "Processing {} in {} for {}".format(
                        sequence, dataset.name, verifier.name))
                sequence_result = {}
                sequence_result['sequence_name'] = sequence
                for result_name in result_list:
                    sequence_result[result_name] = []
                sequence_result['result_label_list'] = []
                sequence_result['result_link_id_list'] = []

                # for each pair
                for pair_idx in range(len(data[sequence]['xs'])):
                    print(pair_idx)
                    data_dict = dataset.get_data_sequence_pair(sequence, pair_idx)
                    est_E = None
                    est_F = None

                    if verifier.estimates_fundamental:
                        est_F = self.find_F_matrix(verifier, data_dict)
                    elif verifier.estimates_essential:
                        est_E = self.find_E_matrix(verifier, data_dict)
                    else:
                        print("check verifier, if doesn't estimat E or F")

                    data_dict['est_E'] = est_E
                    data_dict['est_F'] = est_F

                    result_number_list = self.evaluate_unit(
                        data_dict)
                    sequence_result['result_link_id_list'].append(
                        "{}".format('pair_'+str(pair_idx)))
                    sequence_result['result_label_list'].append(data[sequence]['img1s'][pair_idx])

                    for result_name, result_number in zip(
                            result_list, result_number_list):
                        # for debug
                        #print('{}: {}'.format(result_name, result_number))
                        sequence_result[result_name].append(result_number)

                for result_name in result_list:
                    sequence_result['ave_{}'.format(result_name)] = np.mean(
                        np.array(sequence_result['{}'.format(result_name)]))
                    result['ave_{}'.format(result_name)] = result['ave_{}'.format(
                        result_name)] + sequence_result['ave_{}'.format(result_name)]

                result['sequence_result'].append(sequence_result)
            # get average result
            for result_name in result_list:
                result['ave_{}'.format(result_name)] = result['ave_{}'.format(
                    result_name)] / len(result['sequence_result'])
                # for debug
                #print('ave {} {}'.format(result_name,result['ave_{}'.format(result_name)]))

            if save_result:
                with open(result_file_name, "wb") as output_file:
                    pkl.dump(result, output_file)
        return result

    def print_and_save_result(self, results):
        """
        Print and save result.

        :param results: Result to show
        :type results: dict
        """
        self.print_result(results)
        self.save_result(results)

    @abstractmethod
    def evaluate(self, dataset, detector):
        """
        Main function to run the evaluation wrapper. It could be different for different evaluation

        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor

        See Also
        --------

        evaluate_warpper:
        """
        pass

    @abstractmethod
    def evaluate_unit(self, data_dict):
        """
        TODO
        Single evaluation unit. Given a dictionary of data

        :param feature_1: Feature to run. It can be feature or descriptor.
        :type feature_1: array
        :param feature_2: Feature to run. It can be feature or descriptor.
        :type feature_2: array
        :param task: What to run
        :type task: dict

        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """
        pass
