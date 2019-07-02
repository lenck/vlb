# geom.py ---
#
# Filename: geom.py
# Description:
# Origianl Author: Kwang Moo Yi
# Adapter: Alex Butenko
# Created: Thu Oct  5 14:53:24 2017 (+0200)
# Updated: Fri Jun 6 2019
# Copyright (C)
# Visual Computing Group @ University of Victoria
# Computer Vision Lab @ EPFL

# Code:

import numpy as np
import math

def np_skew_symmetric(v):
    """
    From: https://github.com/vcg-uvic/learned-correspondence-release

    Create cross product matrix for v in R^3
    """
    if len(v.shape) == 1:
        v = np.expand_dims(v, axis=0)

    zero = np.zeros_like(v[:, 0])

    M = np.stack([
        zero, -v[:, 2], v[:, 1],
        v[:, 2], zero, -v[:, 0],
        -v[:, 1], v[:, 0], zero,
    ], axis=1)

    return M

def np_unskew_symmetric(M):
    """
    From: https://github.com/vcg-uvic/learned-correspondence-release

    Inverse cross product matrix to extract underlying vector v in R^3
    """
    v = np.concatenate([
        0.5 * (M[:, 7] - M[:, 5])[None],
        0.5 * (M[:, 2] - M[:, 6])[None],
        0.5 * (M[:, 3] - M[:, 1])[None],
    ], axis=1)

    return v

def get_episqr(x1, x2, dR, dt):
    """
    From: https://github.com/vcg-uvic/learned-correspondence-release

    Get normalized epipolar squared distance of camera normalized coordinates
    correspondences from two images.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    dR: np.array (3x3)
        rotation matrix from img1 to img2
    dt: np.array (3x1)
        translation vector of camera1 center (img1) to camera2 center (img2)

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar squared distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    # Compute Fundamental matrix
    dR = dR.reshape(1, 3, 3)
    dt = dt.reshape(1, 3)
    F = np.repeat(np.matmul(
        np.reshape(np_skew_symmetric(dt), (-1, 3, 3)),
        dR
    ).reshape(-1, 3, 3), num_pts, axis=0)

    x2Fx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(F, x1)).flatten()

    ys = x2Fx1**2

    return ys.flatten()

def get_episym(x1, x2, dR, dt):
    """
    From: https://github.com/vcg-uvic/learned-correspondence-release

    Get normalized epipolar symmetric distance of camera normalized coordinates
    correspondences from two images.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    dR: np.array (3x3)
        rotation matrix from img1 to img2
    dt: np.array (3x1)
        translation vector of camera1 center (img1) to camera2 center (img2)

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar symmetric distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    # Compute Fundamental matrix
    dR = dR.reshape(1, 3, 3)
    dt = dt.reshape(1, 3)
    F = np.repeat(np.matmul(
        np.reshape(np_skew_symmetric(dt), (-1, 3, 3)),
        dR
    ).reshape(-1, 3, 3), num_pts, axis=0)

    x2Fx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(F, x1)).flatten()
    Fx1 = np.matmul(F, x1).reshape(-1, 3)
    Ftx2 = np.matmul(F.transpose(0, 2, 1), x2).reshape(-1, 3)

    ys = x2Fx1**2 * (
        1.0 / (Fx1[..., 0]**2 + Fx1[..., 1]**2) +
        1.0 / (Ftx2[..., 0]**2 + Ftx2[..., 1]**2))

    return ys.flatten()

def get_sampsons(x1, x2, dR, dt):
    """
    From: https://github.com/vcg-uvic/learned-correspondence-release

    Get normalized sampsons distance of camera normalized coordinates
    correspondences from two images.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    dR: np.array (3x3)
        rotation matrix from img1 to img2
    dt: np.array (3x1)
        translation vector of camera1 center (img1) to camera2 center (img2)

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the sampsons distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    # Compute Fundamental matrix
    dR = dR.reshape(1, 3, 3)
    dt = dt.reshape(1, 3)
    F = np.repeat(np.matmul(
        np.reshape(np_skew_symmetric(dt), (-1, 3, 3)),
        dR
    ).reshape(-1, 3, 3), num_pts, axis=0)

    x2Fx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(F, x1)).flatten()
    Fx1 = np.matmul(F, x1).reshape(-1, 3)
    Ftx2 = np.matmul(F.transpose(0, 2, 1), x2).reshape(-1, 3)

    ys = x2Fx1**2 / (
        Fx1[..., 0]**2 + Fx1[..., 1]**2 + Ftx2[..., 0]**2 + Ftx2[..., 1]**2
    )

    return ys.flatten()

def get_episqr_w_matrix(x1, x2, M):
    """
    Adapted from https://github.com/vcg-uvic/learned-correspondence-release

    Get epipolar squared distance of keypoint correspondences between 2 images
    using the correspondence matrix M.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    M: np.array (3x3)
        Matrix relating correspondence between img1 and img2

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar squared distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    M = np.repeat(M.reshape(-1, 3, 3), num_pts, axis=0)

    x2Mx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(M, x1)).flatten()

    ys = x2Mx1**2

    return ys.flatten()

def get_epidist_w_matrix(x1, x2, M):
    """
    Adapted from https://github.com/vcg-uvic/learned-correspondence-release

    Get epipolar distance of keypoint correspondences between 2 images
    using the correspondence matrix M.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    M: np.array (3x3)
        Matrix relating correspondence between img1 and img2

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    M = np.repeat(M.reshape(-1, 3, 3), num_pts, axis=0)

    x2Mx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(M, x1)).flatten()
    Mx1 = np.matmul(M, x1).reshape(-1, 3)


    ys = x2Mx1 * (1.0 / np.sqrt((Mx1[..., 0]**2 + Mx1[..., 1]**2)))

    return np.abs(ys.flatten())

def get_episym_w_matrix(x1, x2, M):
    """
    Adapted from https://github.com/vcg-uvic/learned-correspondence-release

    Get epipolar symmetric distance of keypoint correspondences between 2 images
    using the correspondence matrix M.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    M: np.array (3x3)
        Matrix relating correspondence between img1 and img2

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar symmetric distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    Mt = np.repeat(M.T.reshape(-1, 3, 3), num_pts, axis=0)
    M = np.repeat(M.reshape(-1, 3, 3), num_pts, axis=0)

    x2Mx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(M, x1)).flatten()
    Mx1 = np.matmul(M, x1).reshape(-1, 3)
    Mtx2 = np.matmul(Mt, x2).reshape(-1, 3)

    x1Mtx2 = np.matmul(x1.transpose(0, 2, 1), np.matmul(Mt, x2)).flatten()

    ys = x2Mx1 * (
        1.0 / np.sqrt(Mx1[..., 0]**2 + Mx1[..., 1]**2)) + x1Mtx2 * (
        1.0 / np.sqrt(Mtx2[..., 0]**2 + Mtx2[..., 1]**2))

    return np.abs(ys.flatten())

def get_epidist(x1,x2, M, type='symmetric'):
    """
    Adapted from https://github.com/vcg-uvic/learned-correspondence-release

    Get an epipolar distance metric of keypoint correspondences between 2 images
    using the correspondence matrix M.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    M: np.array (3x3)
        Matrix relating correspondence between img1 and img2
    type: str
        type of epipolar distance metric desired. Current options are 'symmetric' or 'vanilla'.
        Vanilla is one way epipolar distance of keypoint in image 2 to the projected epipolar line

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar distance of correspondence (x1[idx], x2[idx])
    """
    if type =='symmetric':
        return get_episym_w_matrix(x1, x2, M)
    elif type == 'vanilla':
        return get_epidist_w_matrix(x1, x2, M)
    else:
        print('{} not supported'.format(type))
        return

def get_sampsons_w_matrix(x1, x2, M):
    """
    Adapted from https://github.com/vcg-uvic/learned-correspondence-release

    Get sampsons distance of keypoint correspondences between 2 images
    using the correspondence matrix M.

    Inputs
    ------
    x1: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        normalized camera coordinates of img1 keypoints corresponding to img2 keypoints
    M: np.array (3x3)
        Matrix relating correspondence between img1 and img2

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar distance of correspondence (x1[idx], x2[idx])"""
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    M = np.repeat(M.reshape(-1, 3, 3), num_pts, axis=0)

    x2Mx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(M, x1)).flatten()
    Mx1 = np.matmul(M, x1).reshape(-1, 3)
    Mtx2 = np.matmul(M.transpose(0, 2, 1), x2).reshape(-1, 3)

    ys = x2Mx1**2 / (
        Mx1[..., 0]**2 + Mx1[..., 1]**2 + Mtx2[..., 0]**2 + Mtx2[..., 1]**2
    )
    return ys.flatten()

def get_E_matrix(dR, dt):
    """
    Get the corresponding essential matrix between two cameras based on
    rotation and translation

    Inputs
    ------
    dR: np.array (3x3)
        rotation matrix from img1 to img2
    dt: np.array (3,)
        translation vector from img1 to img2

    Output
    ------
    E: np.array (3x3)
        The essential matrix
    """

    E = np.matmul(
        np.reshape(np_skew_symmetric(dt), (-1, 3, 3)),
        dR
    ).reshape(3, 3)
    return E

def get_F_matrix(dR, dt, K1, K2):
    """
    Get the corresponding fundamental matrix between two cameras based on
    rotation, translation, and internal calibration matrices

    Inputs
    ------
    E: np.array (3x3)
        The essential matrix such that x2Ex1 = 0
        where x1 is from camera1 and x2 is from camera2
    K1: np.array (3x3)
        internal calibration matrix of camera1
    K2: np.array (3x3)
        internal calibration matrix of camera2

    Output
    ------
    F: np.array (3x3)
        The fundamental matrix
    """
    E = get_E_matrix(dR, dt)
    F = np.matmul(np.linalg.inv(K2).T, np.matmul(E,np.linalg.inv(K1)))

    return F

def get_F_matrix_from_E(E, K1, K2):
    """
    Get the corresponding fundamental matrix between two cameras based on
    the essential matrix and internal calibration matrices

    Inputs
    ------
    dR: np.array (3x3)
        rotation matrix from img1 to img2
    dt: np.array (3,)
        translation vector from img1 to img2
    K1: np.array (3x3)
        internal calibration matrix of camera1
    K2: np.array (3x3)
        internal calibration matrix of camera2

    Output
    ------
    F: np.array (3x3)
        The fundamental matrix
    """
    F = np.matmul(np.linalg.inv(K2), np.matmul(E,np.linalg.inv(K1)))

    return F

def to_pixel_coords(K, norm_pts):
    """
    Return pixel coordinates from normalized camera coordinates
    using internal calibration matrix

    Inputs
    ------
    K: np.array (3x3)
        internal calibration matrix of the camera
    norm_pts: np.array (Nx2)
        normalized camera coordinates to transform

    Output
    ------
    px_pts: np.array (Nx2)
        points transformed to pixel coordinates

    """
    if len(norm_pts.shape) == 1:
        norm_pts = np.expand_dims(norm_pts, axis=0)
    num_pts = len(norm_pts)

    norm_pts = np.concatenate([
        norm_pts, np.ones((num_pts, 1))
    ], axis=-1)

    px_pts = np.matmul(K, norm_pts.T)[:-1,:]
    return px_pts.T

def to_camera_coords(K, px_pts):
    """
    Return normalized camera coordinates from pixel coordinates
    using internal calibration matrix

    Inputs
    ------
    K: np.array (3x3)
        internal calibration matrix of the camera
    px_pts: np.array (Nx2)
        normalized camera coordinates to transform

    Output
    ------
    norm_pts: np.array (Nx2)
        points transformed to pixel coordinates

    """
    if len(px_pts.shape) == 1:
        px_pts = np.expand_dims(px_pts, axis=0)
    num_pts = len(px_pts)

    px_pts = np.concatenate([
        px_pts, np.ones((num_pts, 1))
    ], axis=-1)

    norm_pts = np.matmul(np.linalg.inv(K), px_pts.T)[:-1,:]
    return norm_pts.T

def get_inliers_F(x1, x2, F, dist_type='symmetric', thresh=1):
    """
    Find the inlier correspondences based on epipolar distance type and threshold

    Inputs
    ------
    x1: np.array (Nx2)
        coordinates of img1 keypoints corresponding to img2 keypoints
    x2: np.array (Nx2)
        coordinates of img1 keypoints corresponding to img2 keypoints
    F: np.array (3x3)
        Matrix relating correspondence between img1 and img2 (assumed to be Fundamental)
    dist_type: str
        type of epipolar distance metric desired. Current options are 'symmetric' or 'vanilla'.
        Vanilla is one way epipolar distance of keypoint in image 2 to the projected epipolar line
    thresh: float
        distance threshold under which a correspondence pair will be considered an inlier

    Output
    ------
    inlier_x1s: np.array (Nx2)
        x1 points that fall under the distance threshold
    inlier_x2s: np.array (Nx2)
        x2 points that fall under the distance threshold
    inlier_mask: np.array (N,)
        binary array marking indices of original x1, x2 correspondences that are inliers
            1: inlier
            0: outlier
    """
    if dist_type == 'vanilla':
        epi_dist = get_epidist_w_matrix(x1, x2, F)
    elif dist_type == 'symmetric':
        epi_dist = get_episym_w_matrix(x1, x2, F)
    else:
        print('{} is not a supported distance type'.format(dist_type))
        return
    inlier_mask = np.zeros(x1.shape[0])
    inlier_mask[epi_dist < thresh] = 1

    inlier_x1s = x1[epi_dist < thresh,:]
    inlier_x2s = x2[epi_dist < thresh,:]
    return inlier_x1s, inlier_x2s, inlier_mask

def get_epi_constraint(x1, x2, F):
    """
    Calculate the epipolar constraint (x2Fx1) of putative corresondences with relation matrix F

    Inputs
    ------
    x1: np.array (Nx2)
        keypoints from img1
    x2: np.array (Nx2)
        keypoints from img2
    F: np.array (3x3)
        relational matrix

    Output
    ------
    ys: np.array (N,)
        ys[idx] is the epipolar constraint distance of correspondence (x1[idx], x2[idx])
    """
    num_pts = len(x1)

    # Make homogeneous coordinates
    x1 = np.concatenate([
        x1, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)
    x2 = np.concatenate([
        x2, np.ones((num_pts, 1))
    ], axis=-1).reshape(-1, 3, 1)

    F = np.repeat(F.reshape(-1, 3, 3), num_pts, axis=0)

    x2Fx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(F, x1)).flatten()

    ys = x2Fx1

    return ys.flatten()


def get_pr_recall(true_inliers, est_inliers):
    """ get the precision and recall from inlier masks """
    tp = np.sum(np.logical_and(true_inliers, est_inliers))
    fp = np.sum(np.logical_and(true_inliers==0, est_inliers==1))
    fn = np.sum(np.logical_and(true_inliers==1, est_inliers==0))
    tn = np.sum(np.logical_and(true_inliers==0, est_inliers==0))

    pr = tp/(tp+fp)
    recall = tp/(tp+fn)

    if math.isnan(pr):
        pr = 0.0
    if math.isnan(recall):
        recall = 0.0
    return pr, recall
# geom.py ends here
