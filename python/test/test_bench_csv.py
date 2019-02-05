import urllib
import tarfile
import os
import sys

sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/dset/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/features/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/bench/')

import vgg_dataset
import vlsift_load_matlab
import my_surf
import repBench
import MatchingScoreBench
import Utils

if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_load_matlab = vlsift_load_matlab.vlsift_load_matlab()
    my_surf = my_surf.my_surf()
    bench = repBench.repBench()
    

    ms_bench = MatchingScoreBench.MatchingScoreBench()
    ms_result_surf = ms_bench.evaluate(vggh,my_surf, use_cache = True, save_result = True)
    ms_result_matlab = ms_bench.evaluate(vggh, vlsift_load_matlab, use_cache = True, save_result = True)

    ms_result = [ms_result_matlab,ms_result_surf]
    for result_term in ms_result[0]['result_term_list']:
        Utils.print_result(ms_result,result_term)
        Utils.save_result(ms_result,result_term)

    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            Utils.print_sequence_result(ms_result,sequence,result_term)
            Utils.save_sequence_result(ms_result, sequence,result_term)
    
