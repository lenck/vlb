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

#sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
#sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
    
class repBench(Benchmark):
    def __init__(self, tmp_feature_dir = './features/', result_dir = './python_scores/'):
        super(repBench,self).__init__(name = 'repeatability', tmp_feature_dir = tmp_feature_dir, result_dir = result_dir)
        
    def evaluate(self, dataset, detector, use_cache = True, save_result = True, norm_factor = 'minab'):
        
        feature_dict = self.detect_feature(dataset,detector, use_cache, save_result)
        try:
            os.makedirs('{}detrep/{}/{}/'.format(self.result_dir, dataset.name, detector.name))
        except:
            pass

        get_result_flag = False
        result_file_name = '{}detrep/{}/{}/repeatability.hkl'.format(self.result_dir, dataset.name, detector.name)
        if use_cache:
            try:
                result = hkl.load(open(result_file_name,'r'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except:
                get_result_flag = False

        if not get_result_flag:
            
            if BenchmarkTemplate.eng is None:
                BenchmarkTemplate.eng = matlab.engine.start_matlab()
                BenchmarkTemplate.eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)
                
            result = {}
            result['dataset_name'] = dataset.name
            result['task_name'] = 'Repeatability'
            result['detector_name'] = detector.name
            result['sequence_result'] = []
            result['ave_repeatability'] = 0.0
            result['norm_factor'] = norm_factor
            pbar = tqdm(dataset)
            for sequence in pbar:
                pbar.set_description("Processing {} in {} for {}".format(sequence.name,dataset.name,detector.name))
                sequence_result = {}
                sequence_result['sequence_name'] = sequence.name
                sequence_result['repeatbility'] = []
                sequence_result['num_cor'] = []
                sequence_result['result_label_list'] = []
                sequence_result['result_link_id_list'] = []
                
                try:
                    result['label'] = sequence.label
                except:
                    pass

                for link in sequence.links():
                    link = link[1]
                    task = link.matlab_task
                    feature_1 = feature_dict['{}_{}'.format(sequence.name, link.source)]
                    feature_2 = feature_dict['{}_{}'.format(sequence.name, link.target)]
                    sequence_result['result_link_id_list'].append("{}_{}".format(link.source, link.target))
                    sequence_result['result_label_list'].append(dataset.get_image(sequence.name, link.target))
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

                            if norm_factor == 'minab':
                                rep = overlapped_num/float(min(fa_num,fb_num))
                            elif norm_factor == 'a':
                                rep = overlapped_num/float(fa_num)
                            elif norm_factor == 'b':
                                rep = overlapped_num/float(fb_num)
                                
                    sequence_result['repeatbility'].append(rep)
                    sequence_result['num_cor'].append(num_cor)

                sequence_result['ave_repeatability'] = np.mean(np.array(sequence_result['repeatbility']))
                result['ave_repeatability'] = result['ave_repeatability']+sequence_result['ave_repeatability']
                result['sequence_result'].append(sequence_result)
            result['ave_repeatability'] = result['ave_repeatability']/len(result['sequence_result'])
            #print('ave repeatbility {}'.format(result['ave_repeatability']))
            if save_result:
                with open(result_file_name, "w") as output_file:
                    hkl.dump(result, output_file)

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
                    cur_score_list.append(result['sequence_result'][sequence_index]['repeatbility'][sorted_idx])
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
