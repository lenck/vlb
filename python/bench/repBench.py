import numpy as np
import json
import os
import hickle as hkl
import BenchmarkTemplate
from BenchmarkTemplate import Benchmark
import matlab.engine
import matlab
import csv
from tqdm import tqdm

import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import plotly.plotly as py

class repBench(Benchmark):
    def __init__(self, tmp_feature_dir = './features/', result_dir = './python_scores/'):
        super(repBench,self).__init__(name = 'Repeatability', tmp_feature_dir = tmp_feature_dir, result_dir = result_dir)
    
    def evaluate_unit(self,feature_1, feature_2, task):
        rep = 0.0
        num_cor = 0
        if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0:
            rep = 0.0
            num_cor = 0
        else:
            tcorr, corr_score, info = BenchmarkTemplate.eng.geom.ellipse_overlap_H(task, matlab.double(np.transpose(feature_1).tolist()),\
                    matlab.double(np.transpose(feature_2).tolist()),nargout=3)
            
            corr_score = np.squeeze(np.array(corr_score))
            if corr_score.size==0:
                rep = 0.0
                num_cor = 0
            else:
                perm_index = np.argsort(corr_score)
                perm_index = perm_index[::-1]
                tcorr = np.array(tcorr)
                tcorr_s = np.transpose(tcorr[:,perm_index])
                fa_valid = np.squeeze(np.array(info['fa_valid']))
                fb_valid = np.squeeze(np.array(info['fb_valid']))
                fa_num = np.sum(fa_valid)
                fb_num = np.sum(fb_valid)
            
                matches = BenchmarkTemplate.eng.vlb_greedy_matching(float(fa_num), float(fb_num), matlab.double(tcorr_s.tolist()))
                matches = np.array(matches)
                overlapped_num = sum(matches[1,:]>0)
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
                use_cache = False, save_result = True)
        result['norm_factor'] = norm_factor
        return result
    
    def print_result_sequence(self,results,sequence_name,figure_num = 1):
        if len(results) == 0:
            return
        sequence_index = -1
        
        result = results[0]

        for idx, sequence_result in enumerate(result['sequence_result']):
            if sequence_name == sequence_result['sequence_name']:
                sequence_index = idx

        if sequence_index<0:
            print("No {} sequence in the results!".format(sequence_name))
            return
        
        link_id_list = result['sequence_result'][sequence_index]['result_link_id_list']
        sorted_index = sorted(range(len(link_id_list)),key=link_id_list.__getitem__)

        #link_id_list = link_id_list[sorted_index]
        link_id_list  = [link_id_list[i] for i in sorted_index]

        score_list = []
        num_cor_list = []
        detector_list = []
        for result in results:
            #print(result['sequence_result'][sequence_index]['sequence_name'])
            if result['sequence_result'][sequence_index]['sequence_name'] != sequence_name:
                print("{} doesn't have the result for sequence {}.".format(result['detector_name'],sequence_name))
                continue
            detector_list.append(result['detector_name'])
            cur_score_list = []
            cur_num_cur_list = []
            for idx, sorted_idx in enumerate(sorted_index):
                if result['sequence_result'][sequence_index]['result_link_id_list'][sorted_idx] == link_id_list[idx]:
                    cur_score_list.append(result['sequence_result'][sequence_index]['repeatability'][sorted_idx])
                    cur_num_cur_list.append(result['sequence_result'][sequence_index]['num_cor'][sorted_idx])
                else:
                    print('Detector {} miss link {} for sequence {}'.format(result['detector_name'],link_id_list[idx],sequence_name))
            score_list.append(cur_score_list)
            num_cor_list.append(cur_num_cur_list)

        color = ['r','g','b','k','y','c']

        plt.figure(figure_num)                # the first figure
        plt.subplot(121)
        for idx,score in enumerate(score_list):
            plt.plot(range(len(score)), score, color[idx%len(color)])
        plt.title('{}-{}({})'.format('Repeatability',results[0]['dataset_name'],sequence_name))
        plt.legend(loc='upper right')
        plt.xticks(range(len(score)),link_id_list, rotation = 45)
        plt.xlabel('label')
        plt.ylabel('Repeatability')
        plt.legend(detector_list)

        plt.figure(figure_num)                # the first figure
        plt.subplot(122)
        for idx,score in enumerate(score_list):
            plt.plot(range(len(score)), score, color[idx%len(color)])
        plt.title('{}-{}({})'.format('#Correspondence',results[0]['dataset_name'],sequence_name))
        plt.legend(loc='upper right')
        plt.xticks(range(len(score)),link_id_list, rotation = 45)
        plt.xlabel('label')
        plt.ylabel('#Correspondence')
        plt.legend(detector_list)

        plt.show()

    def print_result(self,results):
        if len(results) ==0 :
            return
        print("")
        print("Dataset: {}".format(results[0]['dataset_name']))
        print("Task: {}".format(results[0]['task_name']))
        results_str_list = self.get_str_list(results)
        self.print_table(results_str_list)

    def save_result(self,results):
        result_file_csv = csv.writer(open('{}detrep/{}/repeatability_result.csv'.format(self.result_dir, results[0]['dataset_name']), 'w'), delimiter=',')
        results_str_list = self.get_str_list(results)
        for this_str in results_str_list:
            result_file_csv.writerow(this_str)

    def get_str_list(self,results):
        max_detector_name_len = 8
        results_str_list = []
        title_str = []
        title_str.append('Detector')
        result = results[0]
        for sequence_result in result['sequence_result']:
            title_str.append(sequence_result['sequence_name'])
        title_str.append('Ave')
        results_str_list.append(title_str) 
        
        for result in results:
            write_str = []
            write_str.append(result['detector_name'])
            for sequence_result in result['sequence_result']:
                write_str.append(str(sequence_result['ave_repeatability']))
            write_str.append(str(result['ave_repeatability']))
            results_str_list.append(write_str)
            
        return results_str_list
