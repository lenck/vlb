import sys
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(
    0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/bench/')

import Utils
import W1BSBench
import np_sift
import W1BS_dataset


if __name__ == "__main__":

    #vggh = vgg_dataset.vggh_Dataset()
    w1bs = W1BS_dataset.W1BS_Dataset()
    np_sift = np_sift.np_sift()
    bench = W1BSBench.W1BSBench()

    # bench.detect_feature(vggh,vlsift_matlab)
    result = bench.evaluate(w1bs, np_sift, use_cache=True, save_result=True)
    result = [result]
    Utils.print_result(result, 'ap')
    # bench.print_result_sequence(result,'bikes')
    # bench.save_result(result)

    #feature,descriptor = vlsift_all.extract_all(image)
    #print(feature.shape, descriptor.shape)
