"""
vlsift matlab version python wrapper
Author: Xu Zhang
"""

import numpy as np
import cv2
import cyvlfeat
import exifread
import feature_utils
import matlab
import matlab.engine
from DetectorDescriptorTemplate import DetectorAndDescriptor

#eng = matlab.engine.start_matlab()
# eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)

#import pdb


class vlsift_load_matlab(DetectorAndDescriptor):
    def __init__(self, peak_thresh=3.0, Magnif=5.0, csv_flag=True):
        super(
            vlsift_load_matlab,
            self).__init__(
            name='vlsift_load_matlab',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            csv_flag=csv_flag)
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
        # pdb.set_trace()
        image = feature_utils.all_to_gray(image)
        image = image / 255.0
        feature, descriptor = eng.vl_sift(matlab.single(image.tolist(
        )), 'Magnif', self.Magnif, nargout=2)  # peak_thresh=self.peak_thresh,
        feature = np.transpose(np.array(feature))
        descriptor = np.transpose(np.array(descriptor))
        # pdb.set_trace()
        return feature, descriptor
