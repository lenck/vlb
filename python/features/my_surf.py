"""
vlsift matlab version python wrapper
Author: Xu Zhang
"""
from DetectorDescriptorTemplate import DetectorAndDescriptor


class my_surf(DetectorAndDescriptor):
    def __init__(self, peak_thresh=3.0, Magnif=5.0, csv_flag=True):
        super(
            my_surf,
            self).__init__(
            name='my_surf',
            is_detector=True,
            is_descriptor=True,
            is_both=True,
            csv_flag=csv_flag)
        self.peak_thresh = peak_thresh
        self.Magnif = Magnif

    def detect_feature(self, image):
        return None

    def extract_descriptor(self, image, feature):
        return None

    def extract_all(self, image):
        return None, None
