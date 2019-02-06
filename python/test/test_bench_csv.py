import sys
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/dset/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/features/')
sys.path.insert(0, '/home/xuzhang/project/Medifor/code/vlb/python/bench/')

import Utils
import MatchingScoreBench
import repBench
import my_surf
import vlsift_load_matlab
import vgg_dataset


if __name__ == "__main__":
    #define dataset
    vggh = vgg_dataset.vggh_Dataset()

    #define feature
    vlsift_load_matlab = vlsift_load_matlab.vlsift_load_matlab()
    my_surf = my_surf.my_surf()
    
    # repeatability test
    rep_bench = repBench.repBench()
    rep_result_surf = rep_bench.evaluate(
        vggh, my_surf, use_cache=False, save_result=True)
    rep_result_matlab = rep_bench.evaluate(
        vggh, vlsift_load_matlab, use_cache=False, save_result=True)
    #merge result and show
    rep_result = [rep_result_matlab, rep_result_surf]
    for result_term in rep_result[0]['result_term_list']:
        Utils.print_result(rep_result, result_term)
        Utils.save_result(rep_result, result_term)
    
    #match score test
    ms_bench = MatchingScoreBench.MatchingScoreBench()
    ms_result_surf = ms_bench.evaluate(
        vggh, my_surf, use_cache=False, save_result=True)
    ms_result_matlab = ms_bench.evaluate(
        vggh, vlsift_load_matlab, use_cache=False, save_result=True)
    #merge result and show
    ms_result = [ms_result_matlab, ms_result_surf]
    for result_term in ms_result[0]['result_term_list']:
        Utils.print_result(ms_result, result_term)
        Utils.save_result(ms_result, result_term)

    #show result for different sequences
    for sequence in vggh.sequence_name_list:
        for result_term in ms_result[0]['result_term_list']:
            Utils.print_sequence_result(ms_result, sequence, result_term)
            Utils.save_sequence_result(ms_result, sequence, result_term)
