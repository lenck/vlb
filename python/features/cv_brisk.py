import cv2
"""
vlsift cython version
Author: Xu Zhang
"""

import numpy as np
import feature_utils
from DetectorDescriptorTemplate import DetectorAndDescriptor
import sys

sys.path.insert(
    0, './3rdparty/wxbs-descriptors-benchmark/code/descriptors/aux/')


class cv_brisk(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_orb,
            self).__init__(
            name='cv_brisk',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            patch_input=True)
        self.descriptor = None

    def detect_feature(self, image):
        brisk = cv2.BRISK_create()
        features =  brisk.detect(image,None)
        return features

    def extract_descriptor(self, image, feature):
        brisk = cv2.BRISK_create()
        _ , descriptors =  brisk.compute(image, feature)
        return descriptors

    def extract_all(self, image):
        brisk = cv2.BRISK_create()
        feature , descriptors =  brisk.compute(image, feature)
        return (feature, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
