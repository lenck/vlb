"""
OpenCV MSER Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import sys


class cv_mser(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_mser,
            self).__init__(
            name='cv_mser',
            is_detector=True,
            is_descriptor=False,
            is_both=False,
            patch_input=False)
        self.descriptor = None

    def detect_feature(self, image):
        mser = cv2.MSER_create()
        features =  mser.detect(image, None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass

    def extract_descriptor_from_patch(self, patches):
        pass
