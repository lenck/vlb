import utils.w1bs
"""
The module is the wide baseline matching benchmark

Author: Xu Zhang
"""

import numpy as np
import os
import BenchmarkTemplate
from tqdm import tqdm
from BenchmarkTemplate import Benchmark
import sys

sys.path.insert(0, './3rdparty/wxbs-descriptors-benchmark/code')

#import pdb


class W1BSBench(Benchmark):
    def __init__(self, tmp_feature_dir='./features/',
                 result_dir='./python_scores/'):
        super(
            W1BSBench,
            self).__init__(
            name='Baseline Stereo',
            tmp_feature_dir=tmp_feature_dir,
            result_dir=result_dir)
        self.bench_name = 'descbm'
        self.test_name = 'baseline_stereo'

    def evaluate_unit(self, feature_1, feature_2, task):
        _, descriptor_1 = feature_1
        _, descriptor_2 = feature_2
        match_dict, match_matrix = utils.w1bs.match_descriptors(descriptor_1, descriptor_2,
                                                                metric="L2", batch_size=256)
        is_correct = (match_matrix[:, 0] ==
                      match_matrix[:, 1]).astype(np.float32)
        r, p, ap = utils.w1bs.get_recall_and_pecision(match_matrix[:, 3], is_correct, n_pts=100,
                                                      smaller_is_better=True)
        return [ap]

    def evaluate(self, dataset, detector, use_cache=True, save_result=True):
        result = self.evaluate_warpper(dataset, detector, ['ap'], extract_descriptor=True,
                                       use_cache=use_cache, save_result=save_result, custom_extraction=True)
        return result

    def detect_feature_custom(self, dataset, detector,
                              use_cache=False, save_feature=True):
        pass

    def extract_descriptor_custom(
            self, dataset, detector, use_cache=False, save_feature=True):
        feature_dict = {}
        descriptor_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir,
                                          dataset.name, detector.name))
        except BaseException:
            pass

        pbar = tqdm(dataset)
        for sequence in pbar:
            pbar.set_description(
                "Extract feature for {} in {} with {}".format(
                    sequence.name, dataset.name, detector.name))
            for image in sequence.images():
                image = image[1]
                descriptor_file_name = '{}{}/{}/{}_{}_descriptor'.format(self.tmp_feature_dir,
                                                                         dataset.name, detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        descriptor = np.load(descriptor_file_name + '.npy')
                        get_feature_flag = True
                    except BaseException:
                        get_feature_flag = False

                if not get_feature_flag:
                    if detector.csv_flag:
                        descriptor_csv_name = './data/{}/{}/{}/{}-{}.descs.csv'.format(self.tmp_feature_dir, dataset.name,
                                                                                       detector.name, sequence.name, image.idx)
                        descriptor = self.load_csv_feature(descriptor_csv_name)
                    else:
                        h, w = image.image_data.shape
                        n_patches = h / w
                        patches_set = np.zeros((n_patches, w, w, 1))
                        for i in range(n_patches):
                            patches_set[i, :, :, 0] = image.image_data[i *
                                                                       (w): (i + 1) * (w), 0:w]
                        descriptor = detector.extract_descriptor_from_patch(
                            patches_set)

                    if save_feature:
                        np.save(descriptor_file_name, descriptor)

                feature_dict['{}_{}'.format(sequence.name, image.idx)] = {}
                descriptor_dict['{}_{}'.format(
                    sequence.name, image.idx)] = descriptor

        return feature_dict, descriptor_dict
