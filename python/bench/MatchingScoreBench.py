"""
The module is the matching score benchmark

Author: Xu Zhang
"""

import numpy as np
import json
import os
import BenchmarkTemplate
from BenchmarkTemplate import Benchmark
import csv
#import pdb

import matlab
import matlab.engine

class MatchingScoreBench(Benchmark):
    def __init__(self, tmp_feature_dir = './features/', result_dir = './python_scores/', matchGeometry = True):
        super(MatchingScoreBench,self).__init__(name = 'Matching Score', tmp_feature_dir = tmp_feature_dir, result_dir = result_dir)
        self.matchGeometry = matchGeometry
        self.bench_name = 'decmatch'
        self.test_name = 'matching_score'
    
    def evaluate_unit(self,feature_1, feature_2, task):
        ms = 0.0
        num_matches = 0
        rep = 0.0
        num_cor = 0
        feature_1, descriptor_1 = feature_1
        feature_2, descriptor_2 = feature_2
        #print(feature_1.shape)
        #print(descriptor_1.shape)

        if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0\
                or descriptor_1 is None or descriptor_2 is None\
                or descriptor_1.shape[0] == 0 or descriptor_2.shape[0] == 0:
            ms = 0.0
            num_matches = 0
            rep = 0.0
            num_cor = 0
        else:
            tcorr, corr_score, info = BenchmarkTemplate.eng.geom.ellipse_overlap_H(\
                    task, matlab.double(np.transpose(feature_1).tolist()),\
                    matlab.double(np.transpose(feature_2).tolist()), 'maxOverlapError', 0.5, nargout=3)
            corr_score = np.squeeze(np.array(corr_score))
            if corr_score.size==0:
                ms = 0.0
                num_matches = 0
                rep = 0.0
                num_cor = 0
            else:
                #have to use stable sort method, otherwise, result will not be correct
                perm_index = np.argsort(1-corr_score,kind='mergesort')
                tcorr = np.array(tcorr)
                tcorr_s = np.transpose(tcorr[:,perm_index])
                fa_valid = np.squeeze(np.array(info['fa_valid']))
                fb_valid = np.squeeze(np.array(info['fb_valid']))
                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
                geoMatches = BenchmarkTemplate.eng.vlb_greedy_matching(float(fa_num),\
                        float(fb_num), matlab.double(tcorr_s.tolist()))
                geoMatches = np.array(geoMatches)
                #print(geoMatches[:,:10])
                overlapped_num = sum(geoMatches[0,:]>0)
                geoMatches = geoMatches[0,:]
                num_cor = overlapped_num

                if self.norm_factor == 'minab':
                    rep = overlapped_num/float(min(fa_num,fb_num))
                elif self.norm_factor == 'a':
                    rep = overlapped_num/float(fa_num)
                elif self.norm_factor == 'b':
                    rep = overlapped_num/float(fb_num)
               
                #pdb.set_trace()
                feature_1 = feature_1[fa_valid,:]
                descriptor_1 = descriptor_1[fa_valid,:]
                feature_2 = feature_2[fb_valid,:]
                descriptor_2 = descriptor_2[fb_valid,:]
                
                descMatchEdges = BenchmarkTemplate.eng.utls.match_greedy(\
                        matlab.double(np.transpose(descriptor_2).tolist()),\
                        matlab.double(np.transpose(descriptor_1).tolist()))
                descMatchEdges = np.array(descMatchEdges)
                descMatches = np.zeros((descriptor_1.shape[0],))
                
                #Align with matlab index
                for edge in np.transpose(descMatchEdges):
                    descMatches[int(edge[1])-1] = int(edge[0])

                if self.matchGeometry:
                    matches = descMatches
                    for idx, (match, geoMatch) in enumerate(zip(matches,geoMatches)):
                        if match != geoMatch:
                            matches[idx] = 0
                else:
                    geoMatchesList = tcorr.tolist()
                    descMatchesEdgeList = descMatchEdges.tolist()
                    intersection = []
                    for descMatch in descMatchesEdgeList:
                        tmpMatch = [descMatch[1],descMatch[0]]
                        if tmpMatch in geoMatch: 
                            intersection.append(tmpMatch)

                    matches = np.zeros((descriptor_1.shape[0],))
                    for edge in intersection:
                        matches[edge[0]] = edge[1]

                num_matches = sum(matches[:]>0.5)
                #print(matches)
                #print(num_matches)
                if self.norm_factor == 'minab':
                    ms = num_matches/float(min(fa_num,fb_num))
                elif self.norm_factor == 'a':
                    ms = num_matches/float(fa_num)
                elif self.norm_factor == 'b':
                    ms = num_matches/float(fb_num)
            #print((rep, num_cor, ms, num_matches))
        return rep, num_cor, ms, num_matches
    
    def evaluate(self, dataset, detector, use_cache = True, save_result = True, norm_factor = 'minab'):
        self.norm_factor = norm_factor
        result = self.evaluate_warpper(dataset, detector, ['repeatability','num_cor','matching_score','num_matches'],\
                extract_descriptor = True, use_cache = use_cache, save_result = save_result)
        result['norm_factor'] = norm_factor
        result['bench_name'] = self.bench_name
        return result
    
