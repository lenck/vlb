"""
OpenCV KAZE Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import sys


class cv_kaze(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_kaze,
            self).__init__(
            name='cv_kaze',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            patch_input=True)
        self.descriptor = None

    def detect_feature(self, image):
        kaze = cv2.KAZE_create()
        features =  kaze.detect(image,None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        kaze = cv2.KAZE_create()
        features =  kaze.detect(image,None)
        _ , descriptors =  kaze.compute(image, features)
        return descriptors

    def extract_all(self, image):
        kaze = cv2.KAZE_create()
        features =  kaze.detect(image,None)
        features , descriptors =  kaze.compute(image, features)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return (pts, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
