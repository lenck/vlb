"""
This module is a warpper for cyvlsift
"""

import numpy as np
import cv2
import cyvlfeat
import features.feature_utils
from features.DetectorDescriptorTemplate import DetectorAndDescriptor


class cyvlsift_official(DetectorAndDescriptor):
    """A warpper for cyvlsift
    
    Attributes 
    ----------

    peak_thresh: float
        Peak threshold for feature detector
    
    """
    def __init__(self, peak_thresh=0.0):
        super(
            cyvlsift_official,
            self).__init__(
            name='cyvlsift_official',
            is_detector=True,
            is_descriptor=True,
            is_both=True)
        self.peak_thresh = peak_thresh

    def detect_feature(self, image):
        """
        Extract feature from image.
        
        :param image: The image
        :type image: array
        :returns: feature
        :rtype: array(n*d)        
        """
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, magnification=5.0)
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
        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature, descriptor = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, frames=feature, magnification=5.0, compute_descriptor=True)
        return descriptor

    def extract_all(self, image):
        """
        Extract feature and descriptor from image.
        
        :param image: The image
        :type image: array
        :returns: feature, descriptor
        :rtype: array(n*d)     
        """

        new_image = image.astype(np.float32)
        new_image = new_image/255.0
        new_image = feature_utils.all_to_gray(new_image)
        feature, descriptor_vector = cyvlfeat.sift.sift(
            new_image, peak_thresh=self.peak_thresh, magnification=5.0, compute_descriptor=True)
        return feature, descriptor_vector
