"""
file adapted from dump_data.py and config.py in
https://github.com/vcg-uvic/learned-correspondence-release
"""

# config.py ---
#
# Filename: config.py
# Description: Based on argparse usage from
#              https://github.com/carpedm20/DCGAN-tensorflow
# Author: Kwang Moo Yi
# Adapted by: Alex Butenko
# Maintainer:
# Created: Mon Jun 26 11:06:51 2017 (+0200)
# Adapted: Friday Jun 6 3:00:00 2019
# Version:
# Package-Requires: ()
# URL:
# Doc URL:
# Keywords:
# Compatibility:
#
#

# Commentary:
#
#
#
#

# Change Log:
#
#
#

# Code:
import argparse

def str2bool(v):
    return v.lower() in ("true", "1")

arg_lists = []
parser = argparse.ArgumentParser()


def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg


# Data
data_arg = add_argument_group("Data")
data_arg.add_argument(
    "--data_dump_prefix", type=str, default="../datasets/Verification/data_dump", help=""
    "prefix for the dump folder locations")
data_arg.add_argument(
    "--data_tr", type=str, default="reichstag", help=""
    "name of the dataset for train")
data_arg.add_argument(
    "--data_va", type=str, default="reichstag", help=""
    "name of the dataset for valid")
data_arg.add_argument(
    "--data_te", type=str, default="reichstag", help=""
    "name of the dataset for test")
data_arg.add_argument(
    "--data_crop_center", type=str2bool, default=False, help=""
    "whether to crop center of the image "
    "to match the expected input for methods that expect a square input")
data_arg.add_argument(
    "--use_lift", type=str2bool, default=False, help=""
    "if this is set to true, we expect lift to be dumped already for all "
    "images.")


# -----------------------------------------------------------------------------
# Objective
obj_arg = add_argument_group("obj")
obj_arg.add_argument(
    "--obj_num_kp", type=int, default=2000, help=""
    "number of keypoints per image")
obj_arg.add_argument(
    "--obj_top_k", type=int, default=-1, help=""
    "number of keypoints above the threshold to use for "
    "essential matrix estimation. put -1 to use all. ")
obj_arg.add_argument(
    "--obj_num_nn", type=int, default=1, help=""
    "number of nearest neighbors in terms of descriptor "
    "distance that are considered when generating the "
    "distance matrix")
obj_arg.add_argument(
    "--obj_geod_type", type=str, default="episym",
    choices=["sampson", "episqr", "episym"], help=""
    "type of geodesic distance")
obj_arg.add_argument(
    "--obj_geod_th", type=float, default=1e-4, help=""
    "theshold for the good geodesic distance")


# Training
train_arg = add_argument_group("Train")
train_arg.add_argument(
    "--run_mode", type=str, default="train", help=""
    "run_mode")
train_arg.add_argument(
    "--train_batch_size", type=int, default=32, help=""
    "batch size")
train_arg.add_argument(
    "--train_max_tr_sample", type=int, default=10000, help=""
    "number of max training samples")
train_arg.add_argument(
    "--train_max_va_sample", type=int, default=1000, help=""
    "number of max validation samples")
train_arg.add_argument(
    "--train_max_te_sample", type=int, default=1000, help=""
    "number of max test samples")
train_arg.add_argument(
    "--train_lr", type=float, default=1e-3, help=""
    "learning rate")
train_arg.add_argument(
    "--train_iter", type=int, default=500000, help=""
    "training iterations to perform")
train_arg.add_argument(
    "--res_dir", type=str, default="./logs", help=""
    "base directory for results")
train_arg.add_argument(
    "--log_dir", type=str, default="", help=""
    "save directory name inside results")
train_arg.add_argument(
    "--test_log_dir", type=str, default="", help=""
    "which directory to test inside results")
train_arg.add_argument(
    "--val_intv", type=int, default=5000, help=""
    "validation interval")
train_arg.add_argument(
    "--report_intv", type=int, default=1000, help=""
    "summary interval")

# -----------------------------------------------------------------------------
# Visualization
vis_arg = add_argument_group('Visualization')
vis_arg.add_argument(
    "--vis_dump", type=str2bool, default=False, help=""
    "turn this on to dump data for visualization"
)
vis_arg.add_argument(
    "--tqdm_width", type=int, default=79, help=""
    "width of the tqdm bar"
)


def setup_dataset(dataset_name):
    """Expands dataset name and directories properly"""

    # Use only the first one for dump
    dataset_name = dataset_name.split(".")[0]

    data_dir = "../datasets/Verification/datasets/"

    # Expand the abbreviations that we use to actual folder names
    if "cogsci4" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_4---brown_cogsci_4---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.3
    elif "reichstag" == dataset_name:
        # Load the data
        data_dir += "reichstag/"
        geom_type = "Calibration"
        vis_th = 100
    elif "sacre_coeur" == dataset_name:
        # Load the data
        data_dir += "sacre_coeur/"
        geom_type = "Calibration"
        vis_th = 100
    elif "buckingham" in dataset_name:
        # Load the data
        data_dir += "buckingham_palace/"
        geom_type = "Calibration"
        vis_th = 100
    elif "notre_dame" == dataset_name:
        # Load the data
        data_dir += "notre_dame_front_facade/"
        geom_type = "Calibration"
        vis_th = 100
    elif "st_peters" == dataset_name:
        # Load the data
        data_dir += "st_peters_square/"
        geom_type = "Calibration"
        vis_th = 100
    elif "harvard_conf_big" == dataset_name:
        # Load the data
        data_dir += "harvard_conf_big---hv_conf_big_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.3
    elif "home_ac" == dataset_name:
        # Load the data
        data_dir += "home_ac---home_ac_scan1_2012_aug_22---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.3
    elif "fountain" in dataset_name:
        # Load the data
        data_dir += "fountain/"
        geom_type = "Calibration"
        vis_th = -1
    elif "herzjesu" == dataset_name:
        # Load the data
        data_dir += "herzjesu/"
        geom_type = "Calibration"
        vis_th = -1
    elif "gms-teddy" == dataset_name:
        # Load the data
        data_dir += "gms-teddy/"
        geom_type = "Calibration"
        vis_th = 100
    elif "gms-large-cabinet" in dataset_name:
        # Load the data
        data_dir += "gms-large-cabinet/"
        geom_type = "Calibration"
        vis_th = 100
    elif "cogsci8_05" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_8---brown_cogsci_8---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cogsci2_05" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_2---brown_cogsci_2---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_lounge1_2_05" == dataset_name:
        # Load the data
        data_dir += "harvard_corridor_lounge---hv_lounge1_2---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_c10_2_05" == dataset_name:
        # Load the data
        data_dir += "harvard_c10---hv_c10_2---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_s1_2_05" == dataset_name:
        # Load the data
        data_dir += "harvard_robotics_lab---hv_s1_2---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_c4_1_05" == dataset_name:
        # Load the data
        data_dir += "harvard_c4---hv_c4_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cs7_05" == dataset_name:
        # Load the data
        data_dir += "brown_cs_7---brown_cs7---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cs3_05" == dataset_name:
        # Load the data
        data_dir += "brown_cs_3---brown_cs3---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "mit_46_6conf_05" == dataset_name:
        # Load the data
        data_dir += "mit_46_6conf---bcs_floor6_conf_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "mit_46_6lounge_05" == dataset_name:
        # Load the data
        data_dir += "mit_46_6lounge---bcs_floor6_long---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "mit_w85g_05" == dataset_name:
        # Load the data
        data_dir += "mit_w85g---g_0---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "mit_32_g725_05" == dataset_name:
        # Load the data
        data_dir += "mit_32_g725---g725_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "florence_hotel_05" == dataset_name:
        # Load the data
        data_dir += "hotel_florence_jx---florence_hotel_stair_room_all---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "mit_w85h_05" == dataset_name:
        # Load the data
        data_dir += "mit_w85h---h2_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cogsci6_05" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_6---brown_cogsci_6---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    # New sets
    elif "home_ac_05_fix" == dataset_name:
        # Load the data
        data_dir += "home_ac---home_ac_scan1_2012_aug_22---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "harvard_conf_big_05_fix" == dataset_name:
        # Load the data
        data_dir += "harvard_conf_big---hv_conf_big_1---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cogsci3_05" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_3---brown_cogsci_3---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "cogsci4_05_fix" == dataset_name:
        # Load the data
        data_dir += "brown_cogsci_4---brown_cogsci_4---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "home_aca_05_fix" == dataset_name:
        # Load the data
        data_dir += "home_ag---apartment_ag_nov_7_2012_scan1_erika---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hotel_ucsd_05" == dataset_name:
        # Load the data
        data_dir += "hotel_ucsd---la2-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "brown_cs_4_05" == dataset_name:
        data_dir += "brown_cs_4---brown_cs4-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hotel_ucla_ant_05" == dataset_name:
        # Load the data
        data_dir += "hotel_ucla_ant---hotel_room_ucla_scan1_2012_oct_05-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_lounge3_05" == dataset_name:
        data_dir += "harvard_corridor_lounge---hv_lounge_corridor3_whole_floor-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "harvard_conf_big_05_rand" == dataset_name:
        # Load the data
        data_dir += "harvard_conf_big---hv_conf_big_1-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "brown_bm_3_05" == dataset_name:
        # Load the data
        data_dir += "brown_bm_3---brown_bm_3-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "home_pt_05" == dataset_name:
        # Load the data
        data_dir += "home_pt---home_pt_scan1_2012_oct_19-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_comp_05" == dataset_name:
        # Load the data
        data_dir += "harvard_computer_lab---hv_c1_1-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hv_lounge2_05" == dataset_name:
        # Load the data
        data_dir += "harvard_corridor_lounge---hv_lounge_corridor2_1-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5
    elif "hotel_ped_05" == dataset_name:
        # Load the data
        data_dir += "hotel_pedraza---hotel_room_pedraza_2012_nov_25-maxpairs-10000-random---skip-10-dilate-25/"
        geom_type = "Calibration"
        vis_th = 0.5

    return data_dir, geom_type, vis_th


def get_config():
    config, unparsed = parser.parse_known_args()

    # Setup the dataset related things
    for _mode in ["tr", "va", "te"]:
        data_dir, geom_type, vis_th = setup_dataset(
            getattr(config, "data_" + _mode))
        setattr(config, "data_dir_" + _mode, data_dir)
        setattr(config, "data_geom_type_" + _mode, geom_type)
        setattr(config, "data_vis_th_" + _mode, vis_th)

    return config, unparsed


def print_usage():
    parser.print_usage()


#!/usr/bin/env python3
# dump_data.py ---
#
# Filename: dump_data.py
# Description:
# Author: Kwang Moo Yi
# Adapted by: Alex Butenko
# Created: Mon Apr  2 18:33:34 2018 (-0700)
# Adapted: Friday Jun 6 3:00:00 2019
# Version:
# Package-Requires: ()
# URL:
# Doc URL:
# Keywords:
# Compatibility:
#
#

# Commentary:
#
#
#
#

# Change Log:
#
#
#
# Copyright (C)
# Visual Computing Group @ University of Victoria
# Computer Vision Lab @ EPFL

# Code:


from __future__ import print_function

import itertools
import multiprocessing as mp
import os
import pickle
import sys
import time

import numpy as np

import cv2
from data import loadFromDir
from geom import get_episqr, get_episym, get_sampsons, parse_geom
from six.moves import xrange
from utils import loadh5, saveh5

eps = 1e-10
use3d = False
config = None

config, unparsed = get_config()


def dump_data_pair(args):
    dump_dir, idx, ii, jj, queue = args

    # queue for monitoring
    if queue is not None:
        queue.put(idx)

    dump_file = os.path.join(
        dump_dir, "idx_sort-{}-{}.h5".format(ii, jj))

    if not os.path.exists(dump_file):
        # Load descriptors for ii
        desc_ii = loadh5(
            os.path.join(dump_dir, "kp-z-desc-{}.h5".format(ii)))["desc"]
        desc_jj = loadh5(
            os.path.join(dump_dir, "kp-z-desc-{}.h5".format(jj)))["desc"]
        # compute decriptor distance matrix
        distmat = np.sqrt(
            np.sum(
                (np.expand_dims(desc_ii, 1) - np.expand_dims(desc_jj, 0))**2,
                axis=2))
        # Choose K best from N
        idx_sort = np.argsort(distmat, axis=1)[:, :config.obj_num_nn]
        idx_sort = (
            np.repeat(
                np.arange(distmat.shape[0])[..., None],
                idx_sort.shape[1], axis=1
            ),
            idx_sort
        )
        distmat = distmat[idx_sort]
        # Dump to disk
        dump_dict = {}
        dump_dict["idx_sort"] = idx_sort
        saveh5(dump_dict, dump_file)


def make_xy(num_sample, pairs, kp, z, desc, img, geom, vis, depth, geom_type,
            cur_folder):

    xs = []
    ys = []
    Rs = []
    ts = []
    img1s = []
    img2s = []
    cx1s = []
    cy1s = []
    f1s = []
    cx2s = []
    cy2s = []
    f2s = []
    k1s = []
    k2s = []

    # Create a random folder in scratch
    dump_dir = os.path.join(cur_folder, "dump")
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)

    # randomly suffle the pairs and select num_sample amount
    np.random.seed(1234)
    cur_pairs = [
        pairs[_i] for _i in np.random.permutation(len(pairs))[:num_sample]
    ]
    idx = 0
    for ii, jj in cur_pairs:
        idx += 1
        print(
            "\rExtracting keypoints {} / {}".format(idx, len(cur_pairs)),
            end="")
        sys.stdout.flush()

        # Check and extract keypoints if necessary
        for i in [ii, jj]:
            dump_file = os.path.join(dump_dir, "kp-z-desc-{}.h5".format(i))
            if not os.path.exists(dump_file):
                if kp[i] is None:
                    cv_kp, cv_desc = sift.detectAndCompute(img[i].transpose(
                        1, 2, 0), None)
                    cx = (img[i][0].shape[1] - 1.0) * 0.5
                    cy = (img[i][0].shape[0] - 1.0) * 0.5
                    # Correct coordinates using K
                    cx += parse_geom(geom, geom_type)["K"][i, 0, 2]
                    cy += parse_geom(geom, geom_type)["K"][i, 1, 2]
                    xy = np.array([_kp.pt for _kp in cv_kp])
                    # Correct focals
                    fx = parse_geom(geom, geom_type)["K"][i, 0, 0]
                    fy = parse_geom(geom, geom_type)["K"][i, 1, 1]
                    kp[i] = (
                        xy - np.array([[cx, cy]])
                    ) / np.asarray([[fx, fy]])
                    desc[i] = cv_desc
                if z[i] is None:
                    cx = (img[i][0].shape[1] - 1.0) * 0.5
                    cy = (img[i][0].shape[0] - 1.0) * 0.5
                    fx = parse_geom(geom, geom_type)["K"][i, 0, 0]
                    fy = parse_geom(geom, geom_type)["K"][i, 1, 1]
                    xy = kp[i] * np.asarray([[fx, fy]]) + np.array([[cx, cy]])
                    if len(depth) > 0:
                        z[i] = depth[i][
                            0,
                            np.round(xy[:, 1]).astype(int),
                            np.round(xy[:, 0]).astype(int)][..., None]
                    else:
                        z[i] = np.ones((xy.shape[0], 1))
                # Write descs to harddisk to parallize
                dump_dict = {}
                dump_dict["kp"] = kp[i]
                dump_dict["z"] = z[i]
                dump_dict["desc"] = desc[i]
                saveh5(dump_dict, dump_file)
            else:
                dump_dict = loadh5(dump_file)
                kp[i] = dump_dict["kp"]
                z[i] = dump_dict["z"]
                desc[i] = dump_dict["desc"]
    print("")

    # Create arguments
    pool_arg = []
    idx = 0
    for ii, jj in cur_pairs:
        idx += 1
        pool_arg += [(dump_dir, idx, ii, jj)]
    # Run mp job
    ratio_CPU = 0.8
    number_of_process = int(ratio_CPU * mp.cpu_count())
    pool = mp.Pool(processes=number_of_process)
    manager = mp.Manager()
    queue = manager.Queue()
    for idx_arg in xrange(len(pool_arg)):
        pool_arg[idx_arg] = pool_arg[idx_arg] + (queue,)
    # map async
    pool_res = pool.map_async(dump_data_pair, pool_arg)
    # monitor loop
    while True:
        if pool_res.ready():
            break
        else:
            size = queue.qsize()
            print("\rDistMat {} / {}".format(size, len(pool_arg)), end="")
            sys.stdout.flush()
            time.sleep(1)
    pool.close()
    pool.join()
    print("")
    # Pack data
    idx = 0
    total_num = 0
    good_num = 0
    bad_num = 0
    for ii, jj in cur_pairs:
        idx += 1
        print("\rWorking on {} / {}".format(idx, len(cur_pairs)), end="")
        sys.stdout.flush()

        # ------------------------------
        # Get dR
        R_i = parse_geom(geom, geom_type)["R"][ii]
        R_j = parse_geom(geom, geom_type)["R"][jj]
        dR = np.dot(R_j, R_i.T)
        # Get dt
        t_i = parse_geom(geom, geom_type)["t"][ii].reshape([3, 1])
        t_j = parse_geom(geom, geom_type)["t"][jj].reshape([3, 1])
        dt = t_j - np.dot(dR, t_i)
        # ------------------------------
        # Get sift points for the first image
        x1 = kp[ii]
        y1 = np.concatenate([kp[ii] * z[ii], z[ii]], axis=1)
        # Project the first points into the second image
        y1p = np.matmul(dR[None], y1[..., None]) + dt[None]
        # move back to the canonical plane
        x1p = y1p[:, :2, 0] / y1p[:, 2, 0][..., None]
        # ------------------------------
        # Get sift points for the second image
        x2 = kp[jj]
        # # DEBUG ------------------------------
        # # Check if the image projections make sense
        # draw_val_res(
        #     img[ii],
        #     img[jj],
        #     x1, x1p, np.random.rand(x1.shape[0]) < 0.1,
        #     (img[ii][0].shape[1] - 1.0) * 0.5,
        #     (img[ii][0].shape[0] - 1.0) * 0.5,
        #     parse_geom(geom, geom_type)["K"][ii, 0, 0],
        #     (img[jj][0].shape[1] - 1.0) * 0.5,
        #     (img[jj][0].shape[0] - 1.0) * 0.5,
        #     parse_geom(geom, geom_type)["K"][jj, 0, 0],
        #     "./debug_imgs/",
        #     "debug_img{:04d}.png".format(idx)
        # )
        # ------------------------------
        # create x1, y1, x2, y2 as a matrix combo
        x1mat = np.repeat(x1[:, 0][..., None], len(x2), axis=-1)
        y1mat = np.repeat(x1[:, 1][..., None], len(x2), axis=1)
        x1pmat = np.repeat(x1p[:, 0][..., None], len(x2), axis=-1)
        y1pmat = np.repeat(x1p[:, 1][..., None], len(x2), axis=1)
        x2mat = np.repeat(x2[:, 0][None], len(x1), axis=0)
        y2mat = np.repeat(x2[:, 1][None], len(x1), axis=0)
        # Load precomputed nearest neighbors
        idx_sort = loadh5(os.path.join(
            dump_dir, "idx_sort-{}-{}.h5".format(ii, jj)))["idx_sort"]
        # Move back to tuples
        idx_sort = (idx_sort[0], idx_sort[1])
        x1mat = x1mat[idx_sort]
        y1mat = y1mat[idx_sort]
        x1pmat = x1pmat[idx_sort]
        y1pmat = y1pmat[idx_sort]
        x2mat = x2mat[idx_sort]
        y2mat = y2mat[idx_sort]
        # Turn into x1, x1p, x2
        x1 = np.concatenate(
            [x1mat.reshape(-1, 1), y1mat.reshape(-1, 1)], axis=1)
        x1p = np.concatenate(
            [x1pmat.reshape(-1, 1),
             y1pmat.reshape(-1, 1)], axis=1)
        x2 = np.concatenate(
            [x2mat.reshape(-1, 1), y2mat.reshape(-1, 1)], axis=1)

        # make xs in NHWC
        xs += [
            np.concatenate([x1, x2], axis=1).T.reshape(4, 1, -1).transpose(
                (1, 2, 0))
        ]

        # ------------------------------
        # Get the geodesic distance using with x1, x2, dR, dt
        if config.obj_geod_type == "sampson":
            geod_d = get_sampsons(x1, x2, dR, dt)
        elif config.obj_geod_type == "episqr":
            geod_d = get_episqr(x1, x2, dR, dt)
        elif config.obj_geod_type == "episym":
            geod_d = get_episym(x1, x2, dR, dt)
        # Get *rough* reprojection errors. Note that the depth may be noisy. We
        # ended up not using this...
        reproj_d = np.sum((x2 - x1p)**2, axis=1)
        # count inliers and outliers
        total_num += len(geod_d)
        good_num += np.sum((geod_d < config.obj_geod_th))
        bad_num += np.sum((geod_d >= config.obj_geod_th))
        ys += [np.stack([geod_d, reproj_d], axis=1)]
        # Save R, t for evaluation
        Rs += [np.array(dR).reshape(3, 3)]
        ts += [np.array(dt).flatten()]

        # Save img1 and img2 for display
        img1s += [img[ii]]
        img2s += [img[jj]]
        cx = (img[ii][0].shape[1] - 1.0) * 0.5
        cy = (img[ii][0].shape[0] - 1.0) * 0.5
        # Correct coordinates using K
        K1 = parse_geom(geom, geom_type)["K"][ii]
        cx += K1[0, 2]
        cy += K1[1, 2]
        fx = K1[0, 0]
        fy = K1[1, 1]
        if np.isclose(fx, fy):
            f = fx
        else:
            f = (fx, fy)
        cx1s += [cx]
        cy1s += [cy]
        f1s += [f]
        cx = (img[jj][0].shape[1] - 1.0) * 0.5
        cy = (img[jj][0].shape[0] - 1.0) * 0.5
        # Correct coordinates using K
        K2 = parse_geom(geom, geom_type)["K"][jj]
        cx += K2[0, 2]
        cy += K2[1, 2]
        fx = K2[0, 0]
        fy = K2[1, 1]
        if np.isclose(fx, fy):
            f = fx
        else:
            f = (fx, fy)
        cx2s += [cx]
        cy2s += [cy]
        f2s += [f]
        k1s += [K1]
        k2s += [K2]

    # Do *not* convert to numpy arrays, as the number of keypoints may differ
    # now. Simply return it
    print(".... done")
    if total_num > 0:
        print(" Good pairs = {}, Total pairs = {}, Ratio = {}".format(
            good_num, total_num, float(good_num) / float(total_num)))
        print(" Bad pairs = {}, Total pairs = {}, Ratio = {}".format(
            bad_num, total_num, float(bad_num) / float(total_num)))

    res_dict = {}
    res_dict["xs"] = xs
    res_dict["ys"] = ys
    res_dict["Rs"] = Rs
    res_dict["ts"] = ts
    res_dict["img1s"] = img1s
    res_dict["cx1s"] = cx1s
    res_dict["cy1s"] = cy1s
    res_dict["f1s"] = f1s
    res_dict["img2s"] = img2s
    res_dict["cx2s"] = cx2s
    res_dict["cy2s"] = cy2s
    res_dict["f2s"] = f2s
    res_dict["K1s"] = k1s
    res_dict["K2s"] = k2s

    return res_dict


print("-------------------------DUMP-------------------------")
print("Note: dump_data.py will only work on the first dataset")

# Read conditions
crop_center = config.data_crop_center
data_folder = config.data_dump_prefix
if config.use_lift:
    data_folder += "_lift"

# Prepare opencv
print("Creating Opencv SIFT instance")
if not config.use_lift:
    sift = cv2.xfeatures2d.SIFT_create(
        nfeatures=config.obj_num_kp, contrastThreshold=1e-5)

# Now start data prep
print("Preparing data for {}".format(config.data_tr.split(".")[0]))

# Commented out as this takes a long time to process
# for _set in ["train", "valid", "test"]:

# Currently using test set to save time
for _set in ["test"]:
    num_sample = getattr(
        config, "train_max_{}_sample".format(_set[:2]))

    # Load the data
    print("Loading Raw Data for {}".format(_set))
    if _set == "valid":
        split = "val"
    else:
        split = _set
    img, geom, vis, depth, kp, desc = loadFromDir(
        getattr(config, "data_dir_" + _set[:2]) + split + "/",
        "-16x16",
        bUseColorImage=True,
        crop_center=crop_center,
        load_lift=config.use_lift)
    if len(kp) == 0:
        kp = [None] * len(img)
    if len(desc) == 0:
        desc = [None] * len(img)
    z = [None] * len(img)

    # Generating all possible pairs
    print("Generating list of all possible pairs for {}".format(_set))
    pairs = []
    for ii, jj in itertools.product(xrange(len(img)), xrange(len(img))):
        if ii != jj:
            if vis[ii][jj] > getattr(config, "data_vis_th_" + _set[:2]):
                pairs.append((ii, jj))
    print("{} pairs generated".format(len(pairs)))

    # Create data dump directory name
    data_names = getattr(config, "data_" + _set[:2])
    data_name = data_names.split(".")[0]
    cur_data_folder = "/".join([
        data_folder,
        data_name,
        "numkp-{}".format(config.obj_num_kp),
        "nn-{}".format(config.obj_num_nn),
    ])
    if not config.data_crop_center:
        cur_data_folder = os.path.join(cur_data_folder, "nocrop")
    if not os.path.exists(cur_data_folder):
        os.makedirs(cur_data_folder)
    suffix = "{}-{}".format(
        _set[:2], getattr(config, "train_max_" + _set[:2] + "_sample"))
    cur_folder = os.path.join(cur_data_folder, suffix)
    if not os.path.exists(cur_folder):
        os.makedirs(cur_folder)

    # Check if we've done this folder already.
    print(" -- Waiting for the data_folder to be ready")
    ready_file = os.path.join(cur_folder, "ready")
    if not os.path.exists(ready_file):
        print(" -- No ready file {}".format(ready_file))
        print(" -- Generating data")

        # Make xy for this pair
        data_dict = make_xy(
            num_sample, pairs, kp, z, desc,
            img, geom, vis, depth, getattr(
                config, "data_geom_type_" + _set[:2]),
            cur_folder)

        # Let's pickle and save data. Note that I'm saving them
        # individually. This was to have flexibility, but not so much
        # necessary.
        for var_name in data_dict:
            cur_var_name = var_name + "_" + _set[:2]
            out_file_name = os.path.join(cur_folder, cur_var_name) + ".pkl"
            with open(out_file_name, "wb") as ofp:
                pickle.dump(data_dict[var_name], ofp)

        # Mark ready
        with open(ready_file, "w") as ofp:
            ofp.write("This folder is ready\n")
    else:
        print("Done!")

#
# dump_data.py ends here
