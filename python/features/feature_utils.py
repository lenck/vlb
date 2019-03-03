#!/usr/bin/python
#-*- coding: utf-8 -*- 
#===========================================================
#  File Name: feature_util.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-26-2019
#  Last Modified: Sat Mar  2 12:23:24 2019
#
#  Description: Detector and descriptor util function
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
# 
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
#===========================================================

"""
This module is a warpper for cyvlsift
"""
import numpy as np
import cv2

def all_to_gray(image):
    """
    Convert image to gray image (Matlab coeffients).
    
    :param image: The image
    :type image: array
    :returns: gray_image
    :rtype: array(w*h)        
    """

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
    """
    Convert image to gray image (opencv coeffients).
    
    :param image: The image
    :type image: array
    :returns: gray_image
    :rtype: array(w*h)        
    """

    if len(image.shape) == 2:
        return image
    if image.shape[2] == 4:
        image = image[:, :, :3]
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def all_to_BGR(image):
    """
    Convert image to 3-channel image.
    
    :param image: The image
    :type image: array
    :returns: color_image
    :rtype: array(w*h*3)        
    """

    if image.shape[2] == 1:
        image = np.repeat(image, 3, axis=2)
    if image.shape[2] == 4:
        image = image[:, :, :3]
    return image


def rectify_patch(img, kp, patch_sz=32):
    """
    Extract an rectified patch from image with information in the keypoint.
    
    :param img: The image
    :type img: array
    :param kp: The key point
    :type kp: array
    :param patch_sz: patch size
    :type patch_sz: int 
    :returns: patch
    :rtype: array(w*h)        
    """

    scale = 1.0  # rotate in the patch
    M = cv2.getRotationMatrix2D(
        (patch_sz / 2, patch_sz / 2), -1 * kp[3] * 180 / 3.1415, scale)
    # print(M)
    patch = cv2.warpAffine(img, np.float32(M), (patch_sz, patch_sz),
                         flags=cv2.WARP_INVERSE_MAP + cv2.INTER_CUBIC)
    return patch


def extract_patch(img, kp, patch_sz=32, rectify_flag=False):
    """
    Extract an rectified patch from image with information in the keypoint.
    
    :param img: The image
    :type img: array
    :param kp: The key point
    :type kp: array
    :param patch_sz: patch size
    :type patch_sz: int 
    :param rectify_flag: rectified or not
    :type rectify_flag: boolean
    :returns: patch
    :rtype: array(w*h)        
    """

    sub = cv2.getRectSubPix(img, (int(kp[2] / 2 * patch_sz),
                                  int(kp[2] / 2 * patch_sz)), (kp[1], kp[0]))
    res = cv2.resize(sub, (patch_sz, patch_sz))
    if rectigy_flag:
        res = rectify_patch(res, kp, patch_sz)
    return np.asarray(res)


def rgb2gray(img):
    """
    Convert bgr image to gray image (Matlab coeffients).
    
    :param img: The image
    :type img: array
    :returns: img_gray
    :rtype: array(n*d)        
    """

    img_gray = np.average(img, weights=[0.1140, 0.5870, 0.2989], axis=2)

    return img_gray
