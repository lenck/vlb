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
import MatchingScoreBench
import Utils

if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    #vlsift_all = vlsift.vlsift()
    vlsift_all = vlsift_matlab.vlsift_matlab()
    bench = MatchingScoreBench.MatchingScoreBench()
    #bench = repBench.repBench()
    
    #bench.detect_feature(vggh,vlsift_matlab)
    result = bench.evaluate(vggh, vlsift_all, use_cache = True, save_result = True)
    result = [result]
    for result_term in result[0]['result_term_list']:
        Utils.print_result(result,result_term)
        Utils.save_result(result,result_term)
        Utils.print_result_sequence(result,'boat',result_term)
    #bench.print_result(result)
    #bench.print_result_sequence(result,'bikes')
    #bench.save_result(result)

    #feature,descriptor = vlsift_all.extract_all(image)
    #print(feature.shape, descriptor.shape)
    
