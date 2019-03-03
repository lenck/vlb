#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: DetectorDescriptorTemplate.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sat Mar  2 13:46:34 2019
#
#  Description: Detector and descriptor template
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================


"""
This module describe basic detector and descriptor
"""

import numpy as np
import cv2
import cyvlfeat
import exifread

from abc import ABCMeta, abstractmethod


class DetectorAndDescriptor():
    """Basic template class for detector and descriptor.

    Attributes 
    ----------

    name: str
        Name of the detector
    is_detector: boolean, optional
        Is the module is a detector or not
    is_descriptor: boolean, optional
        Is the module is a descriptor or not
    is_both: boolean, optional
        Is the module is both a detector and a decritpor or not
    csv_flag: boolean, optional
        Can the module load feature from csv file or not
    patch_input: boolean, optional
        Do the module take patch instead of full image as input or not
    """

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
        """
        Extract feature from image.
        
        :param image: The image
        :type image: array
        :returns: feature
        :rtype: array(n*d)        
        """
        pass

    @abstractmethod
    def extract_descriptor(self, image, feature):
        """
        Extract descriptor from image with feature.

        :param image: The image
        :type image: array
        :param feature: The feature output by detector
        :type feature: array
        :returns: descriptor
        :rtype: array(n*d)
        """
        pass

    @abstractmethod
    def extract_all(self, image):
        """
        Extract feature and descriptor from image.
        
        :param image: The image
        :type image: array
        :returns: feature, descriptor
        :rtype: array(n*d)     
        """
        pass


class DetectorDescriptorBundle(DetectorAndDescriptor):
    """
    Combine a detector and a descriptor to make a new detector+descriptor. 
    For paper only focuses on either detector or descriptor.
    
    Attributes 
    ----------

    name: str
        Name of the Bundle
    detector: DetectorAndDescriptor
        The detector to combine
    descriptor: DetectorAndDescriptor
        The descriptor to combine
    """

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
        """
        Extract feature from image.
        
        :param image: The image
        :type image: array
        :returns: feature
        :rtype: array(n*d)
        """

        feature = []
        if self.detector.is_detector:
            feature = detector.detect_feature(image)
        elif self.detector.is_both:
            feature, _ = detector.extract_all(image)
        return feature

    def extract_descriptor(self, image, feature):
        """
        Extract descriptor from image with feature.

        :param image: The image
        :type image: array
        :param feature: The feature output by detector
        :type feature: array
        :returns: descriptor
        :rtype: array(n*d)
        """

        descriptor_vector = []
        if self.descriptor.is_descriptor:
            descriptor_vector = self.descriptor.extract_descriptor(
                image, feature)
        return descriptor_vector

    def extract_all(self, image):
        """
        Extract feature and descriptor from image.
        
        :param image: The image
        :type image: array
        :returns: feature, descriptor
        :rtype: array(n*d)     
        """

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
