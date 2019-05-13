#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: MatchingScoreBench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Mon Apr 15 15:19:28 2019
#
#  Description: Matching score benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

"""
This module describe benchmark for matching score.
"""

import numpy as np
import bench.BenchmarkTemplate
from bench.BenchmarkTemplate import Benchmark
import bench.ellipse_overlap_H
import scipy.io as sio
import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})
import bench.vlb_greedy_matching

class MatchingScoreBench(Benchmark):
    """
    Matching score benchmark
    Return repeatability score, number of correspondence, matching score and number of matches
    """
    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/', matchGeometry=True):
        super(MatchingScoreBench, self).__init__(name='Matching Score',
                                                 tmp_feature_dir=tmp_feature_dir, result_dir=result_dir)
        self.matchGeometry = matchGeometry
        self.bench_name = 'decmatch'
        self.test_name = 'matching_score'

    def evaluate_unit(self, feature_1, feature_2, task):
        """
        Single evaluation unit. Given two features, return the repeatability.

        :param feature_1: Feature and descriptor to run.
        :type feature_1: list of array [feature, descriptor]
        :param feature_2: Feature and descriptor to run.
        :type feature_2: list of array [feature, descriptor]
        :param task: What to run
        :type task: dict

        See Also
        --------

        evaluate_warpper: How to run the unit.
        dset.dataset.Link: definition of task.

        """

        ms = 0.0
        num_matches = 0
        rep = 0.0
        num_cor = 0
        feature_1, descriptor_1 = feature_1
        feature_2, descriptor_2 = feature_2

        if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0\
                or descriptor_1 is None or descriptor_2 is None\
                or descriptor_1.shape[0] == 0 or descriptor_2.shape[0] == 0:
            ms = 0.0
            num_matches = 0
            rep = 0.0
            num_cor = 0
        else:
            option = {}
            option['maxOverlapError'] = 0.5
            geo_info = task
            tcorr, corr_score, info = bench.ellipse_overlap_H.ellipse_overlap_H(
                geo_info, feature_1, feature_2, option)

            if corr_score.size == 0:
                ms = 0.0
                num_matches = 0
                rep = 0.0
                num_cor = 0
            else:
                # have to use stable sort method, otherwise, result will not be
                # correct
                perm_index = np.argsort(1 - corr_score, kind='mergesort')
                tcorr_s = tcorr[perm_index, :]
                fa_valid = info['fa_valid']
                fb_valid = info['fb_valid']

                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
                geoMatches, _ = bench.vlb_greedy_matching.vlb_greedy_matching(
                    fa_num, fb_num, tcorr_s)
                overlapped_num = sum(geoMatches[:, 0] > -1)
                geoMatches = geoMatches[:, 0]
                num_cor = overlapped_num

                if self.norm_factor == 'minab':
                    rep = overlapped_num / float(min(fa_num, fb_num))
                elif self.norm_factor == 'a':
                    rep = overlapped_num / float(fa_num)
                elif self.norm_factor == 'b':
                    rep = overlapped_num / float(fb_num)

                feature_1 = feature_1[fa_valid, :]
                descriptor_1 = descriptor_1[fa_valid, :]
                feature_2 = feature_2[fb_valid, :]
                descriptor_2 = descriptor_2[fb_valid, :]
                descriptor_1.astype(np.float)
                descriptor_2.astype(np.float)

                descMatches = np.zeros(
                    (descriptor_1.shape[0],), dtype=np.int) - 1

                descMatchEdges = bench.ellipse_overlap_H.match_greedy(
                    descriptor_2, descriptor_1)
                for edge in descMatchEdges:
                    descMatches[edge[1]] = edge[0]

                #both descriptor and feature have to be nearest neighbor
                if self.matchGeometry:
                    matches = descMatches
                    for idx, (match, geoMatch) in enumerate(
                            zip(matches, geoMatches)):
                        if match != geoMatch:
                            matches[idx] = -1
                else:
                # only require nearest descriptors has "reasonable" overlap (defined by maxOverlapError) over features.
                    tcorr_set = set()
                    for i in range(tcorr.shape[0]):
                        tcorr_set.add((tcorr[i,0], tcorr[i,1]))
                    descMatchesEdgeList = descMatchEdges.tolist()
                    intersection = []
                    for descMatch in descMatchesEdgeList:
                        tmpMatch = (descMatch[1], descMatch[0])
                        if tmpMatch in tcorr_set:
                            intersection.append(tmpMatch)

                    matches = np.zeros((descriptor_1.shape[0],)) - 1
                    for edge in intersection:
                        matches[edge[0]] = edge[1]

                num_matches = sum(matches[:] > -0.5)

                if self.norm_factor == 'minab':
                    ms = num_matches / float(min(fa_num, fb_num))
                elif self.norm_factor == 'a':
                    ms = num_matches / float(fa_num)
                elif self.norm_factor == 'b':
                    ms = num_matches / float(fb_num)

        return rep, num_cor, ms, num_matches

    def evaluate(self, dataset, detector, use_cache=True,
                 save_result=True, norm_factor='minab'):
        """
        Main function to call the evaluation wrapper. It could be different for different evaluation

        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        :param norm_factor: How to normalize the repeatability. Option: minab, a, b
        :type norm_factor: str
        :returns: result
        :rtype: dict

        See Also
        --------

        bench.Benchmark
        bench.Benchmark.evaluate_warpper:
        """

        self.norm_factor = norm_factor
        result = self.evaluate_warpper(dataset, detector, ['repeatability', 'num_cor', 'matching_score', 'num_matches'],
                                       extract_descriptor=True, use_cache=use_cache, save_result=save_result)
        result['norm_factor'] = norm_factor
        result['bench_name'] = self.bench_name
        return result

    def detect_feature_custom(self, dataset, detector,
                              use_cache=False, save_feature=True):
        """
        Customized feature extraction method. For special task.

        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature
        :rtype: dict

        """

        pass

    def extract_descriptor_custom(
            self, dataset, detector, use_cache=False, save_feature=True):
        """
        Customized description extraction method. For special task.

        :param dataset: Dataset to extract the descriptor
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature
        :rtype: dict

        """

        pass
