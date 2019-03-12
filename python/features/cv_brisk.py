"""
OpenCV BRISK Implementation
Author: Alex Butenko
"""
import cv2
import numpy as np
from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import sys

<<<<<<< HEAD
=======


>>>>>>> eb646e8913abc57fec701bd54369d2b8244a813f
class cv_brisk(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_brisk,
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
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        brisk = cv2.BRISK_create()
        features =  brisk.detect(image,None)
        _ , descriptors =  brisk.compute(image, features)
        return descriptors

    def extract_all(self, image):
        brisk = cv2.BRISK_create()
        features =  brisk.detect(image,None)
        features , descriptors =  brisk.compute(image, features)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return (pts, descriptors)

    def extract_descriptor_from_patch(self, patches):
        pass
