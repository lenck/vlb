"""
Pretrained LIFT Implementation (tensorflow)
Author: Alex Butenko
"""

from features.DetectorDescriptorTemplate import DetectorAndDescriptor
import features.feature_utils as fu

import cv2
import sys
import os
import pickle
import tensorflow as tf
import numpy as np
import importlib
import time
from tqdm import tqdm

import json


dirname = os.path.dirname(__file__)

model_path = dirname+'/tf-lift/release-aug'
if MODEL_PATH not in sys.path:
    sys.path.append(MODEL_PATH)

sys.path.append(dirname+'/tf-lift')

from tf-lift.utils import (IDX_ANGLE, XYZS2kpList, draw_XYZS_to_img, get_patch_size,
                   get_ratio_scale, get_XYZS_from_res_list, restore_network, update_affine)


class LIFT(DetectorAndDescriptor):
    def __init__(self):
        super(
            LIFT,
            self).__init__(
                name='LIFT',
                is_detector=True,
                is_descriptor=True,
                is_both=True,
                patch_input=True)

        self.network = {}
        self.config = {}
        self._set_configs()
        self._build_network('kp')
        self._build_network('desc')

    def _set_configs(self)
        for task in ['kp','desc']:
            self.config[task] =  json.load(open(model_path+'/%s/params.json'%(task),'r')

    def _build_network(self, task)
        tfconfig = tf.ConfigProto()
        tfconfig.gpu_options.allow_growth = True
        self.sess = tf.Session(config=tfconfig)

        # Retrieve mean/std (yes it is hacky)
        logdir = os.path.join(model_path, task)
        if os.path.exists(os.path.join(logdir, "mean.h5")):
            training_mean = loadh5(os.path.join(logdir, "mean.h5"))
            training_std = loadh5(os.path.join(logdir, "std.h5"))

            self.network[task] = Network(self.sess, self.config, self.dataset, {
                                   'mean': training_mean, 'std': training_std})
        else:
            self.network[task] = Network(self.sess, self.config, self.dataset)
        # Make individual saver instances for each module.
        self.saver = {}
        self.best_val_loss = {}
        self.best_step = {}
        # Create the saver instance for both joint and the current subtask
        for _key in ["joint", self.config.subtask]:
            if _key == 'joint':
                self.saver[_key] = tf.train.Saver(self.network.allparams[_key][2:])
            else:
                self.saver[_key] = tf.train.Saver(self.network.allparams[_key])

        # We have everything ready. We finalize and initialie the network here.
        self.sess.run(tf.global_variables_initializer())


    def detect_feature(self, image):
        img = fu.all_to_gray(image)
        kpts, _ = self.run(img)

        return kpts

    def extract_descriptor(self, image, feature):
        img = fu.all_to_gray(image)
        _, desc = self.run(img)

        return desc

    def extract_all(self, image):
        img = fu.all_to_gray(image)
        kpts, desc = self.run(img)

        return (kpts, desc)

    def extract_descriptor_from_patch(self, patches):
        pass

    def close_session(self):
        self.sess.close()

    def _compute_kp(self, image_gray):
        """Compute Keypoints.

        LATER: Clean up code

        """
        # check size
        image_height = image_gray.shape[0]
        image_width = image_gray.shape[1]

        # Multiscale Testing
        scl_intv = self.config['kp'].test_scl_intv
        # min_scale_log2 = 1  # min scale = 2
        # max_scale_log2 = 4  # max scale = 16
        min_scale_log2 = self.config.test_min_scale_log2
        max_scale_log2 = self.config.test_max_scale_log2
        # Test starting with double scale if small image
        min_hw = np.min(image_gray.shape[:2])
        # for the case of testing on same scale, do not double scale
        if min_hw <= 1600 and min_scale_log2!=max_scale_log2:
            print("INFO: Testing double scale")
            min_scale_log2 -= 1
        # range of scales to check
        num_division = (max_scale_log2 - min_scale_log2) * (scl_intv + 1) + 1
        scales_to_test = 2**np.linspace(min_scale_log2, max_scale_log2,
                                        num_division)

        # convert scale to image resizes
        resize_to_test = ((float(self.config.kp_input_size - 1) / 2.0) /
                          (get_ratio_scale(self.config) * scales_to_test))

        # check if resize is valid
        min_hw_after_resize = resize_to_test * np.min(image_gray.shape[:2])
        is_resize_valid = min_hw_after_resize > self.config.kp_filter_size + 1

        # if there are invalid scales and resizes
        if not np.prod(is_resize_valid):
            # find first invalid
            # first_invalid = np.where(True - is_resize_valid)[0][0]
            first_invalid = np.where(~is_resize_valid)[0][0]

            # remove scales from testing
            scales_to_test = scales_to_test[:first_invalid]
            resize_to_test = resize_to_test[:first_invalid]

        # Run for each scale
        test_res_list = []
        for resize in resize_to_test:

            # resize according to how we extracted patches when training
            new_height = np.cast['int'](np.round(image_height * resize))
            new_width = np.cast['int'](np.round(image_width * resize))
            start_time = time.clock()
            image = cv2.resize(image_gray, (new_width, new_height))
            end_time = time.clock()
            resize_time = (end_time - start_time) * 1000.0
            print("Time taken to resize image is {}ms".format(
                resize_time
            ))
            total_time += resize_time

            # run test
            # LATER: Compatibility with the previous implementations
            start_time = time.clock()

            # Run the network to get the scoremap (the valid region only)
            scoremap = None
            if self.config.test_kp_use_tensorflow:
                scoremap = self.network.test(
                    self.config.subtask,
                    image.reshape(1, new_height, new_width, 1)
                ).squeeze()
            else:
                # OpenCV Version
                raise NotImplementedError(
                    "TODO: Implement OpenCV Version")

            end_time = time.clock()
            compute_time = (end_time - start_time) * 1000.0
            test_res_list.append(
                np.pad(scoremap, int((self.config.kp_filter_size - 1) / 2),
                       mode='constant',
                       constant_values=-np.inf)
            )

        # ------------------------------------------------------------------------
        # Non-max suppresion and draw.

        # The nonmax suppression implemented here is very very slow. Consider
        # this as just a proof of concept implementation as of now.

        # Standard nearby : nonmax will check approximately the same area as
        # descriptor support region.
        nearby = int(np.round(
            (0.5 * (self.config.kp_input_size - 1.0) *
             float(self.config.desc_input_size) /
             float(get_patch_size(self.config)))
        ))
        fNearbyRatio = self.config.test_nearby_ratio
        # Multiply by quarter to compensate
        fNearbyRatio *= 0.25
        nearby = int(np.round(nearby * fNearbyRatio))
        nearby = max(nearby, 1)

        nms_intv = self.config.test_nms_intv
        edge_th = self.config.test_edge_th

        res_list = test_res_list

        XYZS = get_XYZS_from_res_list(
            res_list, resize_to_test, scales_to_test, nearby, edge_th,
            scl_intv, nms_intv, do_interpolation=True,
        )
        end_time = time.clock()
        XYZS = XYZS[:self.config.test_num_keypoint]

        kp_list = XYZS2kpList(XYZS)  # note that this is already sorted



    def _compute_desc(self):
        """Compute Descriptors """

        total_time = 0.0

        # Read image
        start_time = time.clock()
        cur_data = self.dataset.load_data()
        end_time = time.clock()
        load_time = (end_time - start_time) * 1000.0
        print("Time taken to load patches is {} ms".format(
            load_time
        ))
        total_time += load_time

        # import IPython
        # IPython.embed()

        # -------------------------------------------------------------------------
        # Test using the test function
        start_time = time.clock()
        descs = self._test_multibatch(cur_data)
        end_time = time.clock()
        compute_time = (end_time - start_time) * 1000.0
        print("Time taken to compute is {} ms".format(
            compute_time
        ))
        total_time += compute_time
        print("Total time for descriptor is {} ms".format(total_time))

        # Overwrite angle
        kps = cur_data["kps"].copy()
        kps[:, 3] = cur_data["angle"][:, 0]

        # Save as h5 file
        save_dict = {}
        # save_dict['keypoints'] = cur_data["kps"]
        save_dict['keypoints'] = kps
        save_dict['descriptors'] = descs
