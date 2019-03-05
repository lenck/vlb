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


class cv_mser(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_orb,
            self).__init__(
            name='cv_mser',
            is_detector=True,
            is_descriptor=False,
            is_both=False,
            patch_input=False)
        self.descriptor = None

    def detect_feature(self, image):
        mser = cv2.MSER_create()
        features =  orb.detect(image,None)
        return features

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass

    def extract_descriptor_from_patch(self, patches):
        pass
