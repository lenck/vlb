"""
vlsift cython version
Author: Xu Zhang
"""

import numpy as np
import json
import os
import cv2
import cyvlfeat
import exifread
import feature_utils 
from DetectorDescriptorTemplate import DetectorAndDescriptor

from abc import ABCMeta, abstractmethod

class vlsift(DetectorAndDescriptor):
    def __init__(self, peak_thresh = 10.0):
        super(vlsift,self).__init__(name = 'vlsift', is_detector = True, is_descriptor = True, is_both = True)
        self.peak_thresh = peak_thresh

    def detect_feature(self, image):
        image = feature_utils.all_to_gray(image)
        feature = cyvlfeat.sift.sift(image, peak_thresh=self.peak_thresh, magnification = 5.0 )#
        return feature

    def extract_descriptor(self, image, feature):
        image = feature_utils.all_to_gray(image)
        feature, descriptor = cyvlfeat.sift.sift(image, peak_thresh=self.peak_thresh, frames=feature, magnification = 5.0, compute_descriptor=True)
        return descriptor
 
    def extract_all(self, image):
        image = feature_utils.all_to_gray(image)
        feature, descriptor_vector = cyvlfeat.sift.sift(image, peak_thresh=self.peak_thresh, magnification = 5.0, compute_descriptor=True)
        return feature, descriptor_vector

