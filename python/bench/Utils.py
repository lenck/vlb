#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: Util.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sun Mar  3 16:43:16 2019
#
#  Description: Writing and printing functions
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

import numpy as np
import os
import csv
from tqdm import tqdm
import cv2

import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
mpl.use('Agg')
import plotly.plotly as py
import matplotlib.pyplot as plt

def draw_sequence_result(results, sequence_name, term_to_show,
                         figure_num=1, result_dir='./python_scores/'):
    if len(results) == 0:
        return
    sequence_index = -1

    result = results[0]

    for idx, sequence_result in enumerate(result['sequence_result']):
        if sequence_name == sequence_result['sequence_name']:
            sequence_index = idx

    if sequence_index < 0:
        print("No {} sequence in the results!".format(sequence_name))
        return

    link_id_list = result['sequence_result'][sequence_index]['result_link_id_list']
    sorted_index = sorted(
        range(
            len(link_id_list)),
        key=link_id_list.__getitem__)

    #link_id_list = link_id_list[sorted_index]
    link_id_list = [link_id_list[i] for i in sorted_index]

    score_list = []
    detector_list = []
    for result in results:
        # print(result['sequence_result'][sequence_index]['sequence_name'])
        if result['sequence_result'][sequence_index]['sequence_name'] != sequence_name:
            print(
                "{} doesn't have the result for sequence {}.".format(
                    result['detector_name'],
                    sequence_name))
            continue
        detector_list.append(result['detector_name'])
        cur_score_list = []
        for idx, sorted_idx in enumerate(sorted_index):
            if result['sequence_result'][sequence_index]['result_link_id_list'][sorted_idx] == link_id_list[idx]:
                cur_score_list.append(
                    result['sequence_result'][sequence_index][term_to_show][sorted_idx])
            else:
                print(
                    'Detector {} miss link {} for sequence {}'.format(
                        result['detector_name'],
                        link_id_list[idx],
                        sequence_name))
        score_list.append(cur_score_list)
    print(score_list)

    color = ['r', 'g', 'b', 'k', 'y', 'c']

    plt.figure(figure_num)                # the first figure
    for idx, score in enumerate(score_list):
        plt.plot(range(len(score)), score, color[idx % len(color)])
    plt.title('{}-{}({})'.format(term_to_show,
                                 results[0]['dataset_name'], sequence_name))
    plt.xticks(range(len(score)), link_id_list, rotation=45)
    plt.xlabel('label')
    plt.ylabel(term_to_show)
    plt.legend(detector_list, loc='upper right')
    plt.savefig('{}{}/{}/{}_{}_result.png'.format(result_dir,
                                                  results[0]['bench_name'], results[0]['dataset_name'], sequence_name, term_to_show))
    plt.clf()


def draw_feature(dataset, sequence_name, image_idx, detector, use_cache=True, figure_num=1,
                 tmp_feature_dir='./features/', result_dir='./python_image/'):

    image = dataset.get_image(sequence_name, image_idx)
    feature_file_name = '{}{}/{}/{}_{}_frame'.format(tmp_feature_dir,
                                                     dataset.name, detector.name, sequence_name, image_idx)

    get_feature_flag = False
    if use_cache:
        try:
            feature = np.load(feature_file_name + '.npy')
            get_feature_flag = True
        except BaseException:
            get_feature_flag = False

    if not get_feature_flag:
        feature = detector.detect_feature(image)

    kp_list = [cv2.KeyPoint(p[1], p[0], p[2], p[3]) for p in feature]

    draw_image = np.copy(image)
    #draw_image = draw_image[...,::-1]
    #draw_image = draw_image.copy()
    if len(draw_image.shape) == 3:
        draw_image = (draw_image[..., ::-1]).copy()

    try:
        os.makedirs('{}{}/{}/'.format(result_dir, dataset.name, detector.name))
    except BaseException:
        pass

    draw_image = cv2.drawKeypoints(
        draw_image,
        kp_list,
        draw_image,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    image_file_name = '{}{}/{}/{}_{}_frame.png'.format(result_dir,
                                                       dataset.name, detector.name, sequence_name, image_idx)

    cv2.imwrite(image_file_name, draw_image)


def print_sequence_result(results, sequence_name, term_to_show):
    if len(results) == 0:
        return
    sequence_index = -1
    result = results[0]
    for idx, sequence_result in enumerate(result['sequence_result']):
        if sequence_name == sequence_result['sequence_name']:
            sequence_index = idx

    if sequence_index < 0:
        print("No {} sequence in the results!".format(sequence_name))
        return

    print("")
    print(
        "Dataset: {}, Sequence: {}".format(
            results[0]['dataset_name'],
            sequence_name))
    print("Metric: {}".format(term_to_show))

    results_str_list = get_sequence_str_list(
        results, sequence_name, term_to_show)
    print_table(results_str_list)


def print_result(results, term_to_show):
    if len(results) == 0:
        return

    print("")
    print("Dataset: {}".format(results[0]['dataset_name']))
    print("Metric: {}".format(term_to_show))
    results_str_list = get_str_list(results, term_to_show)
    print_table(results_str_list)


def print_retrieval_result(results, term_to_show):
    if len(results) == 0:
        return
    print("")
    print("Dataset: {}".format(results[0]['dataset_name']))
    print("Metric: {}".format(term_to_show))
    results_str_list = get_retrieval_str_list(results, term_to_show)

    print_retrieval_table(results_str_list)


def print_retrieval_table(content_list):
    if len(content_list) == 0:
        return

    max_detector_name_len = 8
    max_sequence_name_len = 6

    for content in content_list:
        if len(content[0]) > max_detector_name_len:
            max_detector_name_len = len(content[0])

    content = content_list[0][1:]
    for sequence_name in content:
        if len(sequence_name) > max_sequence_name_len:
            max_sequence_name_len = len(sequence_name)

    content = content_list[0]
    title_str = ''
    for idx, this_str in enumerate(content):
        if idx == 0:
            title_str = "|{}|".format(
                this_str.ljust(max_detector_name_len)[
                    :max_detector_name_len])
        else:
            title_str = title_str + \
                "{}|".format(
                    this_str.ljust(max_sequence_name_len)[
                        :max_sequence_name_len])

    print('-' * len(title_str))
    print(title_str)
    print('-' * len(title_str))
    content_str = ''
    for content in content_list[1:]:
        for idx, this_str in enumerate(content):
            if idx == 0:
                content_str = "|{}|".format(
                    this_str.ljust(max_detector_name_len)[
                        :max_detector_name_len])
            else:
                content_str = content_str + \
                    "{}|".format(
                        this_str.ljust(max_sequence_name_len)[
                            :max_sequence_name_len])
        print(content_str)

    print('-' * len(title_str))


def print_table(content_list):
    if len(content_list) == 0:
        return

    max_detector_name_len = 8
    max_sequence_name_len = 6

    for content in content_list:
        if len(content[0]) > max_detector_name_len:
            max_detector_name_len = len(content[0])

    content = content_list[0][1:]
    for sequence_name in content:
        if len(sequence_name) > max_sequence_name_len:
            max_sequence_name_len = len(sequence_name)

    content = content_list[0]
    title_str = ''
    for idx, this_str in enumerate(content):
        if idx == 0:
            title_str = "|{}|".format(
                this_str.ljust(max_detector_name_len)[
                    :max_detector_name_len])
        else:
            title_str = title_str + \
                "{}|".format(
                    this_str.ljust(max_sequence_name_len)[
                        :max_sequence_name_len])

    print('-' * len(title_str))
    print(title_str)
    print('-' * len(title_str))
    content_str = ''
    for content in content_list[1:]:
        for idx, this_str in enumerate(content):
            if idx == 0:
                content_str = "|{}|".format(
                    this_str.ljust(max_detector_name_len)[
                        :max_detector_name_len])
            else:
                content_str = content_str + \
                    "{}|".format(
                        this_str.ljust(max_sequence_name_len)[
                            :max_sequence_name_len])
        print(content_str)

    print('-' * len(title_str))


def save_result(results, term_to_show, result_dir='./python_scores/'):
    result_file_csv = csv.writer(open('{}{}/{}/{}_result.csv'.format(result_dir,
                                                                     results[0]['bench_name'], results[0]['dataset_name'], term_to_show), 'w'), delimiter=',')
    results_str_list = get_str_list(results, term_to_show)
    for this_str in results_str_list:
        result_file_csv.writerow(this_str)


def save_sequence_result(results, sequence_name,
                         term_to_show, result_dir='./python_scores/'):
    if len(results) == 0:
        return
    sequence_index = -1
    result = results[0]
    for idx, sequence_result in enumerate(result['sequence_result']):
        if sequence_name == sequence_result['sequence_name']:
            sequence_index = idx

    if sequence_index < 0:
        print("No {} sequence in the results!".format(sequence_name))
        return

    result_file_csv = csv.writer(open('{}{}/{}/{}_{}_result.csv'.format(result_dir,
                                                                        results[0]['bench_name'], results[0]['dataset_name'], sequence_name, term_to_show), 'w'), delimiter=',')
    results_str_list = get_sequence_str_list(
        results, sequence_name, term_to_show)
    for this_str in results_str_list:
        result_file_csv.writerow(this_str)


def save_retrieval_result(results, term_to_show,
                          result_dir='./python_scores/'):
    result_file_csv = csv.writer(open('{}{}/{}/{}_result.csv'.format(result_dir,
                                                                     results[0]['bench_name'], results[0]['dataset_name'], term_to_show), 'w'), delimiter=',')
    results_str_list = get_retrieval_str_list(results, term_to_show)
    for this_str in results_str_list:
        result_file_csv.writerow(this_str)


def get_str_list(results, term_to_show):
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
            write_str.append(
                str(sequence_result['ave_{}'.format(term_to_show)]))
        write_str.append(str(result['ave_{}'.format(term_to_show)]))
        results_str_list.append(write_str)

    return results_str_list


def get_sequence_str_list(results, sequence_name, term_to_show):
    sequence_index = -1
    result = results[0]
    for idx, sequence_result in enumerate(result['sequence_result']):
        if sequence_name == sequence_result['sequence_name']:
            sequence_index = idx

    results_str_list = []
    title_str = []
    title_str.append('Detector')

    link_id_list = sequence_result['result_link_id_list']
    sorted_index = sorted(
        range(
            len(link_id_list)),
        key=link_id_list.__getitem__)
    link_id_list = [link_id_list[i] for i in sorted_index]
    for link_id in link_id_list:
        title_str.append(str(link_id))

    title_str.append('Ave')
    results_str_list.append(title_str)

    for result in results:
        write_str = []
        write_str.append(result['detector_name'])
        sequence_result = result['sequence_result'][sequence_index]
        link_id_list = sequence_result['result_link_id_list']
        sorted_index = sorted(
            range(len(link_id_list)),
            key=link_id_list.__getitem__)
        for sorted_idx in sorted_index:
            write_str.append(str(sequence_result[term_to_show][sorted_idx]))
        write_str.append(str(sequence_result['ave_{}'.format(term_to_show)]))
        results_str_list.append(write_str)

    return results_str_list


def get_retrieval_str_list(results, term_to_show):
    results_str_list = []
    title_str = []
    title_str.append('Detector')
    result = results[0]
    title_str.append(term_to_show)
    results_str_list.append(title_str)

    for result in results:
        write_str = []
        write_str.append(result['detector_name'])
        write_str.append(str(result[term_to_show]))
        results_str_list.append(write_str)

    return results_str_list
