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

def print_result_sequence(results, sequence_name, term_to_show, figure_num = 1, result_dir = './python_scores/'):
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
        for idx, sorted_idx in enumerate(sorted_index):
            if result['sequence_result'][sequence_index]['result_link_id_list'][sorted_idx] == link_id_list[idx]:
                cur_score_list.append(result['sequence_result'][sequence_index][term_to_show][sorted_idx])
            else:
                print('Detector {} miss link {} for sequence {}'.format(result['detector_name'],link_id_list[idx],sequence_name))
        score_list.append(cur_score_list)

    color = ['r','g','b','k','y','c']

    plt.figure(figure_num)                # the first figure
    for idx,score in enumerate(score_list):
        plt.plot(range(len(score)), score, color[idx%len(color)])
    plt.title('{}-{}({})'.format(term_to_show,results[0]['dataset_name'],sequence_name))
    plt.xticks(range(len(score)),link_id_list, rotation = 45)
    plt.xlabel('label')
    plt.ylabel(term_to_show)
    plt.legend(detector_list, loc='upper right')
    plt.savefig('{}{}/{}/{}_{}_result.png'.format(result_dir,\
            results[0]['bench_name'], results[0]['dataset_name'], sequence_name, term_to_show))
    plt.clf()

def print_result(results, term_to_show):
    if len(results) ==0 :
        return
    print("")
    print("Dataset: {}".format(results[0]['dataset_name']))
    print("Metric: {}".format(term_to_show))
    results_str_list = get_str_list(results, term_to_show)
    print_table(results_str_list)

def print_table(content_list):
    if len(content_list)==0:
        return

    max_detector_name_len = 8
    max_sequence_name_len = 6

    for content in content_list:
        if len(content[0])>max_detector_name_len:
            max_detector_name_len = len(content[0])

    content = content_list[0][1:]
    for sequence_name in content:
        if len(sequence_name)>max_sequence_name_len:
            max_sequence_name_len = len(sequence_name)

    content = content_list[0]
    title_str = ''
    for idx, this_str in enumerate(content):
        if idx == 0:
            title_str = "|{}|".format(this_str.ljust(max_detector_name_len)[:max_detector_name_len])
        else:
            title_str = title_str+"{}|".format(this_str.ljust(max_sequence_name_len)[:max_sequence_name_len]) 
            
    print('-'*len(title_str))
    print(title_str)
    print('-'*len(title_str))
    content_str = ''
    for content in content_list[1:]:
        for idx, this_str in enumerate(content):
            if idx == 0:
                content_str = "|{}|".format(this_str.ljust(max_detector_name_len)[:max_detector_name_len])
            else:
                content_str = content_str + "{}|".format(this_str.ljust(max_sequence_name_len)[:max_sequence_name_len])
        print(content_str)

    print('-'*len(title_str))

def save_result(results,term_to_show, result_dir = './python_scores/'):
    result_file_csv = csv.writer(open('{}{}/{}/{}_result.csv'.format(result_dir,\
            results[0]['bench_name'], results[0]['dataset_name'], term_to_show), 'w'), delimiter=',')
    results_str_list = get_str_list(results,term_to_show)
    for this_str in results_str_list:
        result_file_csv.writerow(this_str)

def get_str_list(results,term_to_show):
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
            write_str.append(str(sequence_result['ave_{}'.format(term_to_show)]))
        write_str.append(str(result['ave_{}'.format(term_to_show)]))
        results_str_list.append(write_str)
        
    return results_str_list
