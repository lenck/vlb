#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: feature_util.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Mon Feb 18 10:31:14 2019
#
#  Description: Detector and descriptor util function
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================


import numpy as np
import cv2


def all_to_gray(image):
    if len(image.shape) == 2:
        return image
    if image.shape[2] == 4:
        image = image[:, :, :3]
    if image.shape[2] == 3:
        # cv version of color convert seems slightly different from the one in
        # Matlab.
        image = rgb2gray(image)  # cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def all_to_gray_cv(image):
    if len(image.shape) == 2:
        return image
    if image.shape[2] == 4:
        image = image[:, :, :3]
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def all_to_BGR(image):
    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    if image.shape[2] == 4:
        image = image[:, :, :3]
    return image


def rectify_patch(img, kp, patch_sz=32):
    scale = 1.0  # rotate in the patch
    M = cv2.getRotationMatrix2D(
        (patch_sz / 2, patch_sz / 2), -1 * kp[3] * 180 / 3.1415, scale)
    # print(M)
    rot = cv2.warpAffine(img, np.float32(M), (patch_sz, patch_sz),
                         flags=cv2.WARP_INVERSE_MAP + cv2.INTER_CUBIC)
    return rot


def extract_patch(img, kp, patch_sz=32, rectigy_flag=False):
    sub = cv2.getRectSubPix(img, (int(kp[2] / 2 * patch_sz),
                                  int(kp[2] / 2 * patch_sz)), (kp[1], kp[0]))
    res = cv2.resize(sub, (patch_sz, patch_sz))
    if rectigy_flag:
        res = rectify_patch(res, kp, patch_sz)
    return np.asarray(res)


def rgb2gray(img):
    # pdb.set_trace()
    #img_gray = np.average(img, weights=[0.2989, 0.5870, 0.1140], axis=2)
    img_gray = np.average(img, weights=[0.1140, 0.5870, 0.2989], axis=2)
    #img_gray = img_gray.astype(np.uint8)
    return img_gray
