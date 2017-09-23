import numpy as np
import json
import os
import cPickle as pkl
from BenchmarkTemplate import Benchmark
import matlab.engine
import matlab
#sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/dset/')
#sys.path.insert(0, '/Users/Xu/program/Image_Genealogy/code/vlb/python/features/')
    
eng = None
eng = matlab.engine.start_matlab()
eng.addpath(r'/Users/Xu/program/Image_Genealogy/code/vlb/matlab/',nargout=0)

class repBench(Benchmark):
    def __init__(self, tmp_feature_dir = './features/', result_dir = './python_scores/'):
        super(repBench,self).__init__(name = 'repeatability', tmp_feature_dir = tmp_feature_dir, result_dir = result_dir)
        
    def evaluate(self, dataset, detector, use_cache = True, save_result = False, norm_factor = 'minab'):
        
        feature_dict = self.detect_feature(dataset,detector, use_cache, save_result)
        try:
            os.makedirs('{}detrep/{}/{}/'.format(self.result_dir, dataset.name, detector.name))
        except:
            pass

        get_result_flag = False
        result_file_name = '{}detrep/{}/{}/repeatability.pkl'.format(self.result_dir, dataset.name, detector.name)
        if use_cache:
            try:
                feature = pkl.load(feature_file_name)
                get_result_flag = True
            except:
                get_result_flag = False

        if not get_result_flag:
            result = {}
            result['dataset_name'] = dataset.name
            result['task_name'] = 'Repeatability'
            result['detector_name'] = detector.name
            result['sequence_result'] = []
            result['ave_repeatability'] = 0.0
            result['norm_factor'] = norm_factor
            
            for sequence in dataset:
                sequence_result = {}
                sequence_result['sequence_name'] = sequence.name
                sequence_result['repeatbility'] = []
                sequence_result['result_label_list'] = []
                sequence_result['result_link_id_list'] = []
                try:
                    result['label'] = sequence.label
                except:
                    pass

                for link in sequence.links():
                    link = link[1]
                    task = link.matlab_task
                    feature_1 = feature_dict['{}_{}'.format(sequence.name, link.source)]
                    feature_2 = feature_dict['{}_{}'.format(sequence.name, link.target)]
                    sequence_result['result_link_id_list'].append("{}_{}".format(link.source, link.target))
                    sequence_result['result_label_list'].append(dataset.get_image(sequence.name, link.target))
                    rep = 0.0
                    if feature_1 is None or feature_2 is None or feature_1.shape[0] == 0 or feature_2.shape[0] == 0:
                        rep = 0.0
                    else:
                        tcorr, corr_score, info = eng.geom.ellipse_overlap_H(task, matlab.double(np.transpose(feature_1).tolist()),\
                                matlab.double(np.transpose(feature_2).tolist()),nargout=3)
                        
                        corr_score = np.squeeze(np.array(corr_score))
                        if corr_score.size==0:
                            rep = 0.0
                        else:
                            perm_index = np.argsort(corr_score)
                            perm_index = perm_index[::-1]
                            tcorr = np.array(tcorr)
                            tcorr_s = np.transpose(tcorr[:,perm_index])
                            fa_valid = np.squeeze(np.array(info['fa_valid']))
                            fb_valid = np.squeeze(np.array(info['fb_valid']))
                            fa_num = np.sum(fa_valid)
                            fb_num = np.sum(fb_valid)
                        
                            matches = eng.vlb_greedy_matching(float(fa_num), float(fb_num), matlab.double(tcorr_s.tolist()))
                            matches = np.array(matches)
                            overlapped_num = sum(matches[1,:]>0)

                            if norm_factor == 'minab':
                                rep = overlapped_num/float(min(fa_num,fb_num))
                            elif norm_factor == 'a':
                                rep = overlapped_num/float(fa_num)
                            elif norm_factor == 'b':
                                rep = overlapped_num/float(fb_num)
                    print(rep)
                    sequence_result['repeatbility'].append(rep)
                    
                sequence_result['ave_repeatability'] = np.mean(np.array(sequence_result['repeatbility']))
                result['ave_repeatability'] = result['ave_repeatability']+sequence_result['ave_repeatability']
                result['sequence_result'].append(sequence_result)
            result['ave_repeatability'] = result['ave_repeatability']/len(result['sequence_result'])
            print('ave repeatbility {}'.format(result['ave_repeatability']))
            if save_result:
                with open(result_file_name, "wb") as output_file:
                    pkl.dump(d, output_file)

        return 


    def detect_feature(self, dataset, detector, use_cache = False, save_feature = True):
        feature_dict = {}
        try:
            os.makedirs('{}{}/{}/'.format(self.tmp_feature_dir, dataset.name, detector.name))
        except:
            pass

        for sequence in dataset:
            for image in sequence.images():
                image = image[1]
                feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset.name,\
                        detector.name, sequence.name, image.idx)
                get_feature_flag = False
                if use_cache:
                    try:
                        feature = np.load(feature_file_name+'.npy')
                        get_feature_flag = True
                    except:
                        get_feature_flag = False
                        
                if not get_feature_flag:
                    feature = detector.detect_feature(image.image_data)
                    print(feature.shape)
                    if save_feature:
                        np.save(feature_file_name,feature)
                feature_dict['{}_{}'.format(sequence.name,image.idx)] = feature

        return feature_dict

    def load_feature(self, dataset_name, sequence_name, image, detector):
        feature_file_name = '{}{}/{}/{}_{}_frame'.format(self.tmp_feature_dir, dataset_name,\
                        detector.name, sequence_name, image.idx)
        try:
            feature = np.load(feature_file_name)
        except:
            feature = detector.detect_feature(image.image_data)
            np.save(feature_file_name,feature)

        return feature
