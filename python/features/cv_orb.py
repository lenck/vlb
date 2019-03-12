"""
OpenCV ORB Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
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
        features =  orb.detect(image,None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        orb = cv2.ORB_create()
        features =  orb.detect(image,None)
        _ , descriptors = orb.compute(image, features)
        return descriptors

    def extract_all(self, image):
        orb = cv2.ORB_create()
        features =  orb.detect(image,None)
        features, descriptors = orb.compute(image, features)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return (pts, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
