import urllib
import tarfile
import os
import sys

sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')

import vgg_dataset
import vlsift_matlab
import vlsift
import repBench

if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_all = vlsift.vlsift()
    #vlsift_matlab = vlsift_matlab.vlsift_matlab()
    bench = repBench.repBench()
    
    #bench.detect_feature(vggh,vlsift_matlab)
    result = bench.evaluate(vggh,vlsift_all)
    result = [result,result]
    bench.print_result(result)
    bench.save_result(result)

    #feature,descriptor = vlsift_all.extract_all(image)
    #print(feature.shape, descriptor.shape)
    