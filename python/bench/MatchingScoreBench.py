#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: MatchingScoreBench.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Feb  9 10:54:48 2019
#
#  Description: Matching score benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

import numpy as np
import BenchmarkTemplate
from BenchmarkTemplate import Benchmark
import ellipse_overlap_H
import scipy.io as sio
import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})
import vlb_greedy_matching

class MatchingScoreBench(Benchmark):
    def __init__(self, tmp_feature_dir='./features/',
                 result_dir='./python_scores/', matchGeometry=True):
        super(MatchingScoreBench, self).__init__(name='Matching Score',
                                                 tmp_feature_dir=tmp_feature_dir, result_dir=result_dir)
        self.matchGeometry = matchGeometry
        self.bench_name = 'decmatch'
        self.test_name = 'matching_score'

    def evaluate_unit(self, feature_1, feature_2, task):
        ms = 0.0
        num_matches = 0
        rep = 0.0
        num_cor = 0
        feature_1, descriptor_1 = feature_1
        feature_2, descriptor_2 = feature_2
        # print(feature_1.shape)
        # print(descriptor_1.shape)

        if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0\
                or descriptor_1 is None or descriptor_2 is None\
                or descriptor_1.shape[0] == 0 or descriptor_2.shape[0] == 0:
            ms = 0.0
            num_matches = 0
            rep = 0.0
            num_cor = 0
        else:
            # tcorr, corr_score, info = BenchmarkTemplate.eng.geom.ellipse_overlap_H(\
            #        task, matlab.double(np.transpose(feature_1).tolist()),\
            #        matlab.double(np.transpose(feature_2).tolist()), 'maxOverlapError', 0.5, nargout=3)
            #corr_score = np.squeeze(np.array(corr_score))
            option = {}
            option['maxOverlapError'] = 0.5
            geo_info = task
            tcorr, corr_score, info = ellipse_overlap_H.ellipse_overlap_H(
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
                #tcorr = np.array(tcorr)
                #tcorr_s = np.transpose(tcorr[:,perm_index])
                #fa_valid = np.squeeze(np.array(info['fa_valid']))
                #fb_valid = np.squeeze(np.array(info['fb_valid']))

                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
                geoMatches, _ = vlb_greedy_matching.vlb_greedy_matching(
                    fa_num, fb_num, tcorr_s)
                overlapped_num = sum(geoMatches[:, 0] > -1)
                # geoMatches = BenchmarkTemplate.eng.vlb_greedy_matching(float(fa_num),\
                #        float(fb_num), matlab.double(tcorr_s.tolist()))
                #geoMatches = np.transpose(np.array(geoMatches))
                #overlapped_num = sum(geoMatches[:,0]>0)
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
                # descMatchEdges = BenchmarkTemplate.eng.utls.match_greedy(\
                #        matlab.double(np.transpose(descriptor_2).tolist()),\
                #        matlab.double(np.transpose(descriptor_1).tolist()))
                #descMatchEdges = np.array(descMatchEdges)
                # Align with matlab index
                # for edge in np.transpose(descMatchEdges):
                #    descMatches[int(edge[1])-1] = int(edge[0])

                descMatchEdges = ellipse_overlap_H.match_greedy(
                    descriptor_2, descriptor_1)
                for edge in descMatchEdges:
                    descMatches[edge[1]] = edge[0]

                if self.matchGeometry:
                    matches = descMatches
                    for idx, (match, geoMatch) in enumerate(
                            zip(matches, geoMatches)):
                        if match != geoMatch:
                            matches[idx] = -1
                else:
                    tcorr.tolist()
                    descMatchesEdgeList = descMatchEdges.tolist()
                    intersection = []
                    for descMatch in descMatchesEdgeList:
                        tmpMatch = [descMatch[1], descMatch[0]]
                        if tmpMatch in geoMatch:
                            intersection.append(tmpMatch)

                    matches = np.zeros((descriptor_1.shape[0],)) - 1
                    for edge in intersection:
                        matches[edge[0]] = edge[1]

                num_matches = sum(matches[:] > -0.5)
                # print(matches)
                # print(num_matches)
                if self.norm_factor == 'minab':
                    ms = num_matches / float(min(fa_num, fb_num))
                elif self.norm_factor == 'a':
                    ms = num_matches / float(fa_num)
                elif self.norm_factor == 'b':
                    ms = num_matches / float(fb_num)
            #print((rep, num_cor, ms, num_matches))
        return rep, num_cor, ms, num_matches

    def evaluate(self, dataset, detector, use_cache=True,
                 save_result=True, norm_factor='minab'):
        self.norm_factor = norm_factor
        result = self.evaluate_warpper(dataset, detector, ['repeatability', 'num_cor', 'matching_score', 'num_matches'],
                                       extract_descriptor=True, use_cache=use_cache, save_result=save_result)
        result['norm_factor'] = norm_factor
        result['bench_name'] = self.bench_name
        return result

    def detect_feature_custom(self, dataset, detector,
                              use_cache=False, save_feature=True):
        pass

    def extract_descriptor_custom(
            self, dataset, detector, use_cache=False, save_feature=True):
        pass
