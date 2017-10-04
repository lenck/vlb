import numpy as np
import json
import os
import cv2
import cyvlfeat
import exifread

from DetectorDescriptorTemplate import DetectorAndDescriptor

from abc import ABCMeta, abstractmethod

class vlsift(DetectorAndDescriptor):
    def __init__(self, peak_thresh = 3.0):
        super(vlsift,self).__init__(name = 'vlsift', is_detector = True, is_descriptor = True, is_both = True)
        self.peak_thresh = peak_thresh

    def detect_feature(self, image):
        feature = cyvlfeat.sift.sift(img, peak_thresh=self.peak_thresh)
        return feature

    def extract_descriptor(self, image, feature):
        feature, descriptor = cyvlfeat.sift.sift(img, peak_thresh=self.peak_thresh, compute_descriptor=True)
        return descriptor

    def extract_all(self, image):
        feature, descriptor_vector = cyvlfeat.sift.sift(img, peak_thresh=self.peak_thresh, compute_descriptor=True)
        return feature, descriptor_vector

