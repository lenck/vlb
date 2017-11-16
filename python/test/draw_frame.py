import urllib
import tarfile
import os
import sys

sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')

import vgg_dataset
import vlsift
import vlsift_matlab
import Utils

if __name__ == "__main__":

    a = vgg_dataset.vggh_Dataset()
    vlsift_matlab = vlsift_matlab.vlsift_matlab()
    Utils.draw_feature(a,'bikes','1', vlsift_matlab)
