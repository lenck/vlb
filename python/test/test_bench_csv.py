import urllib
import tarfile
import os
import sys

sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/dset/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/features/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/bench/')

import vgg_dataset
import vlsift
import vlsift_load_matlab
import repBench
import MatchingScoreBench
import Utils

if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_all = vlsift.vlsift()
    #vlsift_matlab = vlsift_matlab.vlsift_matlab()
    vlsift_load_matlab = vlsift_load_matlab.vlsift_load_matlab()
    bench = repBench.repBench()
    
    #bench.detect_feature(vggh,vlsift_matlab)
    #result = bench.evaluate(vggh,vlsift_load_matlab,use_cache = False, save_result = True)
    #result = [result]
    #Utils.print_result(result,'repeatability')

    ms_bench = MatchingScoreBench.MatchingScoreBench()
    ms_result_matlab = ms_bench.evaluate(vggh,vlsift_load_matlab, use_cache = False, save_result = True)
    ms_result_python = ms_bench.evaluate(vggh,vlsift_all, use_cache = False, save_result = True)
    ms_result = [ms_result_matlab,ms_result_python]
    for result_term in ms_result[0]['result_term_list']:
        Utils.print_result(ms_result,result_term)
        Utils.save_result(ms_result,result_term)
    #bench.print_result_sequence(result,'bikes')
    #bench.save_result(result)

    #feature,descriptor = vlsift_all.extract_all(image)
    #print(feature.shape, descriptor.shape)
    
