import urllib
import tarfile
import os
import sys
import matlab
import matlab.engine
import numpy as np
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')

import vgg_dataset
import vlsift
import Utils

if __name__ == "__main__":
    eng = matlab.engine.start_matlab()
    eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)
    a = vgg_dataset.vggh_Dataset()
    image = a.get_image('graf','1')
    image = Utils.all_to_gray(image)
    image = image/255.0
    feature_1, descriptor_1 = eng.vl_sift(matlab.single(image.tolist()),nargout = 2)
    feature_1 = np.transpose(np.array(feature_1))
    #print(feature_1[:10,2])
    #vlsift_all = vlsift.vlsift()
    #feature_1, descriptor_1 = vlsift_all.extract_all(image)
    image = a.get_image('graf','2')
    image = Utils.all_to_gray(image)
    image = image/255.0
    feature_2, descriptor_2 = eng.vl_sift(matlab.single(image.tolist()), nargout = 2)
    feature_2 = np.transpose(np.array(feature_2))
    #feature_2, descriptor_2 = vlsift_all.extract_all(image)
    link = a.get_matlab_task('graf','1_2')
    #print(feature_1)
    #print(feature_1.shape)
    #print(feature_1.shape, descriptor_2.shape)
    #print(link)
    #print(np.array(link['H']))

    
    #eng.vlb_setup(nargout=0)

    tcorr, corr_score, info = eng.ellipse_overlap_H(link,matlab.double(np.transpose(feature_1).tolist()),matlab.double(np.transpose(feature_2).tolist()),nargout=3)
    #print(tcorr)
    #print(corr_score)
    #print(info['fa_valid'])
    corr_score = np.squeeze(np.array(corr_score))
    #print(corr_score[:10])
    perm_index = np.argsort(corr_score)
    perm_index = perm_index[::-1]
    print(corr_score[perm_index[:10]])
    tcorr = np.array(tcorr)
    tcorr_s = np.transpose(tcorr[:,perm_index])
    print(tcorr_s.shape)
    #print(tcorr_s)
    
    #tcorr_s = [[179,139],
    #            [179, 140],
    #            [180,139],
    #            [180,140],
    #            [164,126],
    #            [33, 23],
    #            [2, 1],
    #            [147,113],
    #            [78,67],
    #            [5,3],
    #            [74,9],
    #            [74,10],
    #            [132,103],
    #            [140,109],
    #            [141,109],
    #            [75,86]]
    #tcorr_s = np.array(tcorr_s)
    #fa_num = 183
    #fb_num = 143
    
    fa_valid = np.squeeze(np.array(info['fa_valid']))
    fb_valid = np.squeeze(np.array(info['fb_valid']))
    fa_num = np.sum(fa_valid)
    fb_num = np.sum(fb_valid)
    matches = eng.vlb_greedy_matching(float(fa_num), float(fb_num), matlab.double(tcorr_s.tolist()))
    matches = np.array(matches)
    print(matches.shape)
    print(sum(matches[1,:]>0))

