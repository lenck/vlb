#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: test_feature_extraction.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Feb  9 11:13:09 2019
#
#  Usage: python test_feature_extraction.py
#  Description: Test feature extraction
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

import sys

sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(
    0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
import feature_utils
import vlsift_matlab
import vlsift
import vgg_dataset


if __name__ == "__main__":

    a = vgg_dataset.vggh_Dataset()
    image = a.get_image('graf', '1')
    #vlsift_all = vlsift.vlsift()
    vlsift_all = vlsift_matlab.vlsift_matlab()
    feature, descriptor = vlsift_all.extract_all(image)
    print(feature.shape, descriptor.shape)
