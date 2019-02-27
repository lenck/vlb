"""
vlsift cython version
Author: Xu Zhang
"""

import numpy as np
import cv2
import cyvlfeat
import feature_utils
from DetectorDescriptorTemplate import DetectorAndDescriptor


class cyvlsift_official(DetectorAndDescriptor):
    def __init__(self, peak_thresh=0):
        super(
            cyvlsift_official,
            self).__init__(
            name='cyvlsift_official',
            is_detector=True,
            is_descriptor=True,
            is_both=True)
        self.peak_thresh = peak_thresh

    def detect_feature(self, image):
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, magnification=5.0)
        return feature

    def extract_descriptor(self, image, feature):
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature, descriptor = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, frames=feature, magnification=5.0, compute_descriptor=True)
        return descriptor

    def extract_all(self, image):
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature, descriptor_vector = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, magnification=5.0, compute_descriptor=True)
        return feature, descriptor_vector
