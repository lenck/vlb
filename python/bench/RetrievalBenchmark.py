#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: RetrievalBenchmark.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Mar  5 14:11:40 2019
#
#  Description: retrieval benchmark
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

"""
This module describe benchmark for image retrieval.
"""

import numpy as np
from abc import ABCMeta
import os
from tqdm import tqdm
import pickle as pkl
import nmslib
import cv2
import copy


class RetrievalBenchmark():
    __metaclass__ = ABCMeta
    
    """Retrieval Benchmark 
    
    Attributes
    ----------

    name: str
        Name of the dataset
    tmp_feature_dir: str
        Directory for saving the feature
    result_dir: str
        Directory for saving the final result
    """

    def __init__(self, tmp_feature_dir='./data/features/',
                 result_dir='./python_scores/'):
        self.name = "Retrieval"
        self.bench_name = 'Retrieval'
        self.test_name = 'map'
        self.tmp_feature_dir = tmp_feature_dir
        self.result_dir = result_dir

    def extract_descriptor(self, dataset, detector,
                           use_cache=False, save_feature=True):
        """
        Extract descriptors from images.
        
        :param dataset: Dataset to extract the descriptor
        :type dataset: RetrievalDataset
        :param detector: Detector used to extract the descriptor
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_feature: Save computated feature or not
        :type save_feature: boolean
        :returns: feature, descriptor 
        :rtype: dict, dict
        """

        feature_dict = {}
        descriptor_dict = {}

        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir,
                                          dataset.name, detector.name))
        except BaseException:
            pass

        pbar = tqdm(dataset.gallery_list)
        for image_filepath in pbar:
            directory, filename = os.path.split(image_filepath)
            base_filename = os.path.basename(filename)
            feature_file_name = '{}{}/{}/{}_frame'.format(self.tmp_feature_dir,
                                                          dataset.name, detector.name, base_filename)
            descriptor_file_name = '{}{}/{}/{}_descriptor'.format(self.tmp_feature_dir,
                                                                  dataset.name, detector.name, base_filename)
            get_feature_flag = False
            if use_cache:
                try:
                    feature = np.load(feature_file_name + '.npy')
                    descriptor = np.load(descriptor_file_name + '.npy')
                    get_feature_flag = True
                except BaseException:
                    get_feature_flag = False

            if not get_feature_flag:
                image = cv2.imread(image_filepath)
                if image is None:
                    feature = []
                    descriptor = np.array([])
                else:
                    if detector.csv_flag:
                        feature_csv_name = './data/{}/{}/{}/{}.frames.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                  detector.name, base_filename)
                        feature = self.load_csv_feature(feature_csv_name)
                        descriptor_csv_name = './data/{}/{}/{}/{}.descs.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                    detector.name, base_filename)
                        descriptor = self.load_csv_feature(descriptor_csv_name)
                    else:
                        if detector.is_both:
                            feature, descriptor = detector.extract_all(image)
                        else:
                            feature = detector.detect_feature(image)
                            descriptor = detector.extract_descriptor(
                                image, feature=feature)
                if save_feature:
                    np.save(feature_file_name, feature)
                    np.save(descriptor_file_name, descriptor)
            feature_dict[base_filename] = feature
            descriptor_dict[base_filename] = descriptor

        return feature_dict, descriptor_dict

    def load_csv_feature(self, csv_feature_file):
        """
        Load feature from csvfile.
        
        :param csv_feature_file: csv file to load feature
        :type csv_feature_file: str
        :returns: feature
        :rtype: array
        """
        feature = []
        with open(csv_feature_file) as f:
            for line in f:
                tmp_list = line.split(';')
                float_list = [float(i) for i in tmp_list]
                feature.append(float_list)
        return np.asarray(feature)

    # Evaluation warpper
    def evaluate_warpper(self, dataset, detector, result_list, l2_norm=True,
                         use_cache=True, save_result=True, custom_extraction=False):

        """
        Load descriptor from cached file. If failed, extract descriptor from image.

        **Structure of the result:**

        result['dataset_name']: name of the dataset

        result['result_term_list']: list of metrics for evaluation

        result['task_name']: name of the task

        result['detector_name']: name of the dataset

        result['ave_{}']: average value for each metric over all sequences


        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param result_list: Metric to calculate
        :type result_list: list
        :param l2_norm: Perform l2 normalization to descriptor or not
        :type l2_norm: boolean
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        :param custom_extraction: Use custom extraction method or not. See also  and extract_descriptor_custom
        :type custom_extraction: boolean
        :returns: result 
        :rtype: dict

        See Also
        --------

        detect_feature_custom: Extract feature with customized method (special evaluation).
        extract_descriptor_custom: Extract descriptor with customized (special evaluation).

        """

        get_result_flag = False
        result_file_name = '{}{}/{}/{}/{}.pkl'.format(
            self.result_dir, self.bench_name, dataset.name, detector.name, self.test_name)

        try:
            os.makedirs('{}{}/{}/{}/'.format(self.result_dir,
                                             self.bench_name, dataset.name, detector.name))
        except BaseException:
            pass

        result = {}
        if use_cache:
            try:
                result = pkl.load(open(result_file_name, 'rb'))
                print('Get cached result from {}'.format(result_file_name))
                get_result_flag = True
            except BaseException:
                get_result_flag = False

        if not get_result_flag:
            if custom_extraction:
                feature_dict, descriptor_dict = self.extract_descriptor_custom(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)
            else:
                feature_dict, descriptor_dict = self.extract_descriptor(
                    dataset, detector, use_cache=use_cache, save_feature=save_result)

            result = {}
            result['dataset_name'] = dataset.name
            result['result_term_list'] = result_list
            result['task_name'] = self.name
            result['detector_name'] = detector.name
            result['sequence_result'] = []

            desc_list = []
            filename_list = []
            point_list = []
            image_begin_list = []
            image_end_list = []
            feature_index = 0
            image_index = 0
            pbar = dataset.gallery_list
            for image_filepath in pbar:
                directory, filename = os.path.split(image_filepath)
                base_filename = os.path.basename(filename)
                kp = feature_dict[base_filename]
                desc = copy.copy(descriptor_dict[base_filename])
                if kp is None or len(kp) == 0:
                    filename_list.append(base_filename)
                    image_begin_list.append(feature_index)
                    image_end_list.append(feature_index)
                    image_index += 1
                    continue
                else:
                    filename_list.append(base_filename)
                    image_begin_list.append(feature_index)
                    feature_index = feature_index + desc.shape[0]
                    image_end_list.append(feature_index)
                    point_list.extend([image_index] * desc.shape[0])
                    if l2_norm:
                        desc = desc.astype(np.float32)
                        desc /= (desc.sum(axis=1, keepdims=True) + 1e-7)
                        desc = np.sqrt(desc)
                        desc_p = pow(desc, 2)
                        desc /= np.sqrt(desc_p.sum(axis=1,
                                                   keepdims=True) + 1e-7)
                    for i in range(desc.shape[0]):
                        desc_list.append(desc[i, :])
                image_index += 1

            desc_list = np.array(desc_list)

            expand = 3
            nn = 30

            index = nmslib.init(space='l2', method='hnsw')
            index.addDataPointBatch(data=desc_list)
            index.createIndex(
                print_progress=True,
                index_params={
                    "maxM": 32,
                    "maxM0": 64,
                    "indexThreadQty": 24})
            index.setQueryTimeParams(params={"ef": nn * expand})

            query_result = []

            pbar = tqdm(dataset.query_list)
            filter_flag = False
            for query_idx, image_filepath in enumerate(pbar):
                if len(image_filepath) == 5:
                    image_filepath, left, top, bottom, right = image_filepath
                    filter_flag = True

                directory, filename = os.path.split(image_filepath)
                base_filename = os.path.basename(filename)
                kp = feature_dict[base_filename].copy()
                desc = descriptor_dict[base_filename].copy()
                if l2_norm:
                    desc = desc.astype(np.float32)
                    desc /= (desc.sum(axis=1, keepdims=True) + 1e-7)
                    desc = np.sqrt(desc)
                    desc_p = pow(desc, 2)
                    desc /= np.sqrt(desc_p.sum(axis=1, keepdims=True) + 1e-7)
                if filter_flag:
                    new_kp = []
                    new_desc = []
                    for kp_idx, point in enumerate(kp):
                        if point[0] >= left and point[0] <= right and point[1] >= top and point[1] <= bottom:
                            new_kp.append(point)
                            new_desc.append(desc[kp_idx, :])
                    kp = np.array(new_kp)
                    desc = np.array(new_desc)

                if kp is None or len(kp) == 0:
                    result[base_filename] = 0
                    continue

                I = index.knnQueryBatch(queries=desc, k=nn, num_threads=8)
                I = np.array(I)
                D = I[:, 1, :]
                I = I[:, 0, :]
                I = I.astype(int)

                flat_I = I.reshape(I.shape[0] * I.shape[1])
                image_index = [point_list[i] for i in flat_I]
                flat_D = D.reshape(D.shape[0] * D.shape[1])

                sorted_index, sorted_score, sorted_count, score_dict, count_dict = self.get_sorted_index_and_score(
                    image_index, flat_D)

                old_recall = 0.0
                old_precision = 1.0
                ap = 0.0
                good_number = 0
                total_count = 0

                for idx_t, idx in enumerate(sorted_index):
                    if filename_list[idx] in dataset.junk_lists[query_idx]:
                        continue
                    total_count += 1
                    if filename_list[idx] in dataset.positive_lists[query_idx]:
                        good_number += 1
                    recall = good_number / \
                        float(len(dataset.positive_lists[query_idx]))
                    precision = good_number / float(total_count)
                    ap += (recall - old_recall) * \
                        (old_precision + precision) / 2.0
                    old_precision = precision
                    old_recall = recall
                query_result.append(ap)

            result['sequence_result'].append(query_result)

            for result_name in result_list:
                result['m{}'.format(result_name)] = np.mean(
                    np.array(result['sequence_result'][0]))

            if save_result:
                with open(result_file_name, "wb") as output_file:
                    pkl.dump(result, output_file)
        return result

    def print_and_save_result(results):
        """
        Print and save result.

        :param results: Result to show
        :type results: dict
        """

        self.print_retrieval_result(results, 'ap')
        self.save_retrieval_result(results, 'ap')

    def evaluate(self, dataset, detector, use_cache=True, save_result=True):
        """
        Main function to run the evaluation wrapper. It could be different for different evaluation
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean

        See Also
        --------

        evaluate_warpper:
        """

        result = self.evaluate_warpper(dataset, detector, ['ap'],
                                       use_cache=use_cache, save_result=save_result)
        result['bench_name'] = self.bench_name
        return result
    
    def get_sorted_index_and_score(self, image_index, flat_D):
        """
        Given local feature to image index and distance to each local features, return image score
        
        :param dataset: Dataset to extract the feature
        :type dataset: SequenceDataset
        :param detector: Detector used to extract the feature
        :type detector: DetectorAndDescriptor
        :param use_cache: Load cached feature and result or not
        :type use_cache: boolean
        :param save_result: Save result or not
        :type save_result: boolean
        
        :returns: sorted_index, sorted_score, sorted_count, score_dict, count_dict 
        :rtype: array, array, array, dict, dict

        return sorted image index based on score, sorted score, sorted number of matched point, 
        dict of image id to score, dict of image id to number of matched points.

        """
        uidx, counts = np.unique(np.array(image_index), return_counts=True)
        count_dict = dict(zip(uidx, counts))
        score_idx = dict(zip(uidx, range(len(uidx))))
        score_list = np.zeros(len(uidx))

        flat_D = np.maximum(0, pow((1 - np.maximum(0, flat_D - 0.1) / 0.2), 3))

        for temp_idx, dis in zip(image_index, flat_D):
            ind_t = score_idx[temp_idx]
            score_list[ind_t] = score_list[ind_t] + dis
        score_dict = dict(zip(uidx, score_list.tolist()))
        neg_score_list = -1 * score_list

        ridx = range(len(uidx))
        ridx = list(ridx)
        ridx.sort(key=(neg_score_list.tolist().__getitem__))
        sorted_score = score_list[ridx].tolist()
        sorted_count = counts[ridx].tolist()
        sorted_index = uidx[ridx].tolist()

        return sorted_index, sorted_score, sorted_count, score_dict, count_dict
