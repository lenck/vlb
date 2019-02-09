#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: draw_frame.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Sat Feb  9 11:09:58 2019
#
#  Usage: python draw_frame.py
#  Description: Draw frame of the feature
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
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')

import Utils
import vlsift_matlab
import vlsift
import vgg_dataset


if __name__ == "__main__":

    a = vgg_dataset.vggh_Dataset()
    vlsift_matlab = vlsift_matlab.vlsift_matlab()
    Utils.draw_feature(a, 'bikes', '1', vlsift_matlab)
