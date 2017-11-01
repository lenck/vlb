"""
The module is the repeatability benchmark

Author: Xu Zhang
"""

import numpy as np
import json
import os
import hickle as hkl
import BenchmarkTemplate
from BenchmarkTemplate import Benchmark
import csv

import matlab
import matlab.engine

class repBench(Benchmark):
    def __init__(self, tmp_feature_dir = './features/', result_dir = './python_scores/'):
        super(repBench,self).__init__(name = 'Repeatability', tmp_feature_dir = tmp_feature_dir, result_dir = result_dir)
        self.bench_name = 'decrep'
        self.test_name = 'repeatability'
        
    def evaluate_unit(self,feature_1, feature_2, task):
        rep = 0.0
        num_cor = 0
        if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0:
            rep = 0.0
            num_cor = 0
        else:
            tcorr, corr_score, info = BenchmarkTemplate.eng.geom.ellipse_overlap_H(task, matlab.double(np.transpose(feature_1).tolist()),\
                    matlab.double(np.transpose(feature_2).tolist()), 'maxOverlapError', 0.5, nargout=3)
            
            corr_score = np.squeeze(np.array(corr_score))
            if corr_score.size==0:
                rep = 0.0
                num_cor = 0
            else:
                #have to use stable sort method
                perm_index = np.argsort(1-corr_score,kind='mergesort')
                tcorr = np.array(tcorr)
                tcorr_s = np.transpose(tcorr[:,perm_index])
                fa_valid = np.squeeze(np.array(info['fa_valid']))
                fb_valid = np.squeeze(np.array(info['fb_valid']))
                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
            
                matches = BenchmarkTemplate.eng.vlb_greedy_matching(float(fa_num), float(fb_num), matlab.double(tcorr_s.tolist()))
                matches = np.array(matches)
                overlapped_num = sum(matches[0,:]>0)
                num_cor = overlapped_num

                if self.norm_factor == 'minab':
                    rep = overlapped_num/float(min(fa_num,fb_num))
                elif self.norm_factor == 'a':
                    rep = overlapped_num/float(fa_num)
                elif self.norm_factor == 'b':
                    rep = overlapped_num/float(fb_num)

        return rep, num_cor
    
    def evaluate(self, dataset, detector, use_cache = True, save_result = True, norm_factor = 'minab'):
        self.norm_factor = norm_factor
        result = self.evaluate_warpper(dataset, detector, ['repeatability','num_cor'], extract_descriptor = False,\
                use_cache = use_cache, save_result = save_result)
        result['norm_factor'] = norm_factor
        result['bench_name'] = self.bench_name
        return result
