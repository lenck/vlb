"""
vlsift matlab version python wrapper
Author: Xu Zhang
"""

import numpy as np
import cv2
import features.feature_utils
from features.DetectorDescriptorTemplate import DetectorAndDescriptor


class vlsift_load_matlab(DetectorAndDescriptor):
    def __init__(self, csv_flag=True):
        super(
            vlsift_load_matlab,
            self).__init__(
            name='vlsift_load_matlab',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            csv_flag=csv_flag)

    def detect_feature(self, image):
        pass

    def extract_descriptor(self, image, feature):
        pass

    def extract_all(self, image):
        pass
