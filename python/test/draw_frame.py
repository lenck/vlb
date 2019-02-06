import Utils
import vlsift_matlab
import vlsift
import vgg_dataset
import sys

sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(
    0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')


if __name__ == "__main__":

    a = vgg_dataset.vggh_Dataset()
    vlsift_matlab = vlsift_matlab.vlsift_matlab()
    Utils.draw_feature(a, 'bikes', '1', vlsift_matlab)
