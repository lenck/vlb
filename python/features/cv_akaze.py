"""
OpenCV AKAZE Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import sys

sys.path.insert(
    0, './3rdparty/wxbs-descriptors-benchmark/code/descriptors/aux/')


class cv_akaze(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_akaze,
            self).__init__(
            name='cv_akaze',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            patch_input=True)
        self.descriptor = None

    def detect_feature(self, image):
        akaze = cv2.AKAZE_create()
        features =  akaze.detect(image,None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        akaze = cv2.AKAZE_create()
        features =  akaze.detect(image,None)
        _ , descriptors =  akaze.compute(image, features)
        return descriptors

    def extract_all(self, image):
        akaze = cv2.AKAZE_create()
        features =  akaze.detect(image,None)
        features , descriptors =  akaze.compute(image, features)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return (pts, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
