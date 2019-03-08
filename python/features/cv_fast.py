"""
OpenCV FAST Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import sys

sys.path.insert(
    0, './3rdparty/wxbs-descriptors-benchmark/code/descriptors/aux/')


class cv_fast(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_fast,
            self).__init__(
            name='cv_fast',
            is_detector=True,
            is_descriptor=False,
            is_both=False,
            patch_input=True)
        self.descriptor = None

    def detect_feature(self, image):
        fast = cv2.FastFeatureDetector_create()
        features =  fast.detect(image,None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass

    def extract_descriptor_from_patch(self, patches):
        pass
