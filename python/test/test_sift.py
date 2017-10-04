import urllib
import tarfile
import os
import sys

sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')

import vgg_dataset
import vlsift
import vlsift_matlab
import feature_utils

if __name__ == "__main__":

    a = vgg_dataset.vggh_Dataset()
    image = a.get_image('graf','1')
    #vlsift_all = vlsift.vlsift()
    vlsift_all = vlsift_matlab.vlsift_matlab()
    feature,descriptor = vlsift_all.extract_all(image)
    print(feature.shape, descriptor.shape)
    
