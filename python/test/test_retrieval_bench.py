import os
import sys

cwd = os.getcwd()
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import Utils
import RetrievalBenchmark
import repBench
import vlsift
import oxford5k_dataset
import paris6k_dataset


if __name__ == "__main__":

    paris6k = paris6k_dataset.paris6k_Dataset()
    oxford5k = oxford5k_dataset.oxford5k_Dataset()
    vlsift_py = vlsift.vlsift()
    retrieval_bench = RetrievalBenchmark.RetrievalBenchmark()

    map_result_py = retrieval_bench.evaluate(
        paris6k, vlsift_py, use_cache=True, save_result=True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        Utils.print_retrieval_result(map_result, 'm' + result_term)
        Utils.save_retrieval_result(map_result, 'm' + result_term)

    map_result_py = retrieval_bench.evaluate(
        oxford5k, vlsift_py, use_cache=True, save_result=True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        Utils.print_retrieval_result(map_result, 'm' + result_term)
        Utils.save_retrieval_result(map_result, 'm' + result_term)
