"""
vlsift cython version
Author: Xu Zhang
"""

import numpy as np
import json
import os
import feature_utils 
from DetectorDescriptorTemplate import DetectorAndDescriptor
from abc import ABCMeta, abstractmethod
import sys

sys.path.insert(0, './3rdparty/wxbs-descriptors-benchmark/code/descriptors/aux/')
from numpy_sift import SIFTDescriptor

class np_sift(DetectorAndDescriptor):
    def __init__(self, peak_thresh = 10.0):
        super(np_sift,self).__init__(name = 'np_sift', is_detector = True, is_descriptor = True, is_both = True, patch_input = True)
        self.peak_thresh = peak_thresh
        self.descriptor = None

    def detect_feature(self, image):
        pass

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass

    def extract_descriptor_from_patch(self, patches):
        patch_num = patches.shape[0]
        h = patches.shape[1]
        w = patches.shape[2]
        if self.descriptor is None or self.descriptor.patchSize!=w:
            self.descriptor = SIFTDescriptor(w)
        descriptors = np.zeros((patch_num, 128))
        for i in range(patch_num):
            patch = feature_utils.all_to_gray(patches[i,:,:,:])
            patch = patch[:,:,0]
            descriptors[i,:] = self.descriptor.describe(patch).flatten()
        return descriptors
