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


class cv_orb(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_orb,
            self).__init__(
            name='cv_orb',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            patch_input=True)
        self.descriptor = None

    def detect_feature(self, image):
        orb = cv2.ORB_create()
        feature =  orb.detect(image,None)


    def extract_descriptor(self, image, feature):
        orb = cv2.ORB_create()
        _ , descriptors = cv2.compute(image, features)
        return descriptors

    def extract_all(self, image):
        orb = cv2.ORB_create()
        features , descriptors = cv2.compute(image, features)
        return (features, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
