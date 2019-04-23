"""
OpenCV SURF Implementation
Author: Alex Butenko
"""
from DetectorDescriptorTemplate import DetectorAndDescriptor

import cv2
import numpy as np

class cv_surf(DetectorAndDescriptor):
    def __init__(self):
        super(
            cv_surf,
            self).__init__(
                name='cv_surf',
                is_detector=True,
                is_descriptor=True,
                is_both=True)


    def detect_feature(self, image):
        surf = cv2.SURF()
        features =  surf.detect(image, None)
        pts = np.array([features[idx].pt for idx in range(len(features))])
        return pts

    def extract_descriptor(self, image, feature):
        surf = cv2.SURF()
        descriptors =  surf.compute(image, feature)
        return descriptors

    def extract_all(self, image):
        surf = cv2.SURF()
        features, descriptors =  surf.detectAndCompute(image, None)
        return (features, descriptors)
