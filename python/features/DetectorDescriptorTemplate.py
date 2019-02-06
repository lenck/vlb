"""
The module is the detector and descriptor wrapper

Author: Xu Zhang
"""

import numpy as np
import cv2
import cyvlfeat
import exifread

from abc import ABCMeta, abstractmethod


class DetectorAndDescriptor():
    __metaclass__ = ABCMeta

    def __init__(self, name, is_detector=False, is_descriptor=False,
                 is_both=True, csv_flag=False, patch_input=False):
        self.name = name
        self.is_detector = is_detector
        self.is_descriptor = is_descriptor
        self.is_both = is_both
        self.csv_flag = csv_flag
        self.patch_input = patch_input

    @abstractmethod
    def detect_feature(self, image):
        pass

    @abstractmethod
    def extract_descriptor(self, image, feature):
        pass

    @abstractmethod
    def extract_all(self, image):
        pass


class DetectorDescriptorBundle(DetectorAndDescriptor):
    def __init__(self, detector, descriptor):
        self.name = "{}_{}".format(detector.name, descriptor.name)
        self.detector = detector
        self.descriptor = descriptor
        if not self.detector.is_detector and not self.detector.is_both:
            print('Detector has to be a detector!')
            exit()
        if not self.descriptor.is_descriptor:
            print('Descriptor has to be a descriptor!')
            exit()

    def detect_feature(self, image):
        feature = []
        if self.detector.is_detector:
            feature = detector.detect_feature(image)
        elif self.detector.is_both:
            feature, _ = detector.extract_all(image)
        return feature

    def extract_descriptor(self, image, feature):
        descriptor_vector = []
        if self.descriptor.is_descriptor:
            descriptor_vector = self.descriptor.extract_descriptor(
                image, feature)
        return descriptor_vector

    def extract_all(self, image):
        feature = []
        if self.detector.is_detector:
            feature = detector.detect_feature(image)
        elif self.detector.is_both:
            feature, _ = detector.extract_all(image)

        descriptor_vector = []
        if self.descriptor.is_descriptor:
            descriptor_vector = self.descriptor.extract_descriptor(
                image, feature)

        return feature, descriptor_vector
