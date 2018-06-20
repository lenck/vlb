import urllib
import tarfile
import os
import sys

cwd = os.getcwd()
sys.path.insert(0, '{}/python/dset/'.format(cwd))
sys.path.insert(0, '{}/python/features/'.format(cwd))
sys.path.insert(0, '{}/python/bench/'.format(cwd))

import oxford5k_dataset
import vlsift
import repBench
import RetrievalBenchmark
import Utils

if __name__ == "__main__":

    oxford5k = oxford5k_dataset.oxford5k_Dataset()
    vlsift_py = vlsift.vlsift()
    retrieval_bench = RetrievalBenchmark.RetrievalBenchmark()
    
    map_result_py = retrieval_bench.evaluate(oxford5k, vlsift_py, use_cache = True, save_result = True)
    map_result = [map_result_py]
    for result_term in map_result[0]['result_term_list']:
        Utils.print_retrieval_result(map_result, 'm'+result_term)
        Utils.save_retrieval_result(map_result, 'm'+result_term)
