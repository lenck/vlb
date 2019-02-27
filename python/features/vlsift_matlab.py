"""
vlsift matlab version python wrapper
Author: Xu Zhang
"""

import numpy as np
import cv2
import feature_utils
import matlab
import matlab.engine
from DetectorDescriptorTemplate import DetectorAndDescriptor

eng = matlab.engine.start_matlab()
eng.addpath(r'./matlab/', nargout=0)


class vlsift_matlab(DetectorAndDescriptor):
    def __init__(self, peak_thresh=3.0, Magnif=5.0):
        super(
            vlsift_matlab,
            self).__init__(
            name='vlsift_matlab',
            is_detector=True,
            is_descriptor=True,
            is_both=True)
        self.peak_thresh = peak_thresh
        self.Magnif = Magnif

    def detect_feature(self, image):
        image = feature_utils.all_to_gray(image)
        image = image / 255.0
        feature, descriptor = eng.vl_sift(matlab.single(image.tolist(
        )), 'Magnif', self.Magnif, nargout=2)  # , peak_thresh=self.peak_thresh
        feature = np.transpose(np.array(feature))
        return feature

    def extract_descriptor(self, image, feature):
        image = feature_utils.all_to_gray(image)
        image = image / 255.0
        feature, descriptor = eng.vl_sift(matlab.single(image.tolist(
        )), 'Magnif', self.Magnif, nargout=2)  # , peak_thresh=self.peak_thresh
        descriptor = np.transpose(np.array(descriptor))
        return descriptor

    def extract_all(self, image):
        image = feature_utils.all_to_gray(image)
        image = image / 255.0
        feature, descriptor = eng.vl_sift(matlab.single(image.tolist(
        )), 'Magnif', self.Magnif, nargout=2)  # peak_thresh=self.peak_thresh,
        feature = np.transpose(np.array(feature))
        descriptor = np.transpose(np.array(descriptor))
        # pdb.set_trace()
        return feature, descriptor
