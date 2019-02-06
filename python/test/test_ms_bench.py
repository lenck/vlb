import os
import sys
cwd = os.getcwd()
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import Utils
import MatchingScoreBench
import repBench
import vlsift
import vgg_dataset

#import vlsift_matlab

if __name__ == "__main__":

    vggh = vgg_dataset.vggh_Dataset()
    vlsift_py = vlsift.vlsift()
    #vlsift_mat = vlsift_matlab.vlsift_matlab()
    ms_bench = MatchingScoreBench.MatchingScoreBench()
    #rep_bench = repBench.repBench()

    ms_result_py = ms_bench.evaluate(
        vggh, vlsift_py, use_cache=False, save_result=True)
    #ms_result_mat = ms_bench.evaluate(vggh, vlsift_mat, use_cache = True, save_result = True)
    ms_result = [ms_result_py, ms_result_py]
    for result_term in ms_result[0]['result_term_list']:
        Utils.print_result(ms_result, result_term)
        Utils.save_result(ms_result, result_term)
        # Utils.print_result_sequence(ms_result,'boat',result_term)

    #rep_result_py = rep_bench.evaluate(vggh, vlsift_py, use_cache = True, save_result = True)
    #rep_result_mat = rep_bench.evaluate(vggh, vlsift_mat, use_cache = True, save_result = True)
    #rep_result = [rep_result_py,rep_result_mat]
    # for result_term in rep_result[0]['result_term_list']:
    #    Utils.print_result(rep_result,result_term)
    #    Utils.save_result(rep_result,result_term)
    #    Utils.print_result_sequence(rep_result,'boat',result_term)
