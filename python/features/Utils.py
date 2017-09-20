import numpy as np
import json
import os
import cv2


def all_to_gray(image):
    if image.shape[2] == 4:
        image = image[:,:,:3]
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    return image

def all_to_BGR(image):
