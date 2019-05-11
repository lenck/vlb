# geom.py ---
#
# Filename: geom.py
# Description:
# Author: Kwang Moo Yi
# Maintainer:
# Created: Thu Oct  5 14:53:24 2017 (+0200)
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

import numpy as np

def np_skew_symmetric(v):
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

    v = np.concatenate([
        0.5 * (M[:, 7] - M[:, 5])[None],
        0.5 * (M[:, 2] - M[:, 6])[None],
        0.5 * (M[:, 3] - M[:, 1])[None],
    ], axis=1)

    return v


def get_episqr(x1, x2, dR, dt):

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

    return ys.flatten()


def get_episym_w_matrix(x1, x2, M):

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

    return ys.flatten()

def get_epidist(x1,x2, M, type):
    if type =='symmetric':
        return get_episym_w_matrix(x1, x2, M)
    elif type == 'vanilla':
        return get_epidist_w_matrix(x1, x2, M)

    else:
        print('{} not supported'.format(type))
        return

def get_sampsons_w_matrix(x1, x2, M):

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
    E = np.matmul(
        np.reshape(np_skew_symmetric(dt), (-1, 3, 3)),
        dR
    ).reshape(3, 3)
    return E

def get_F_matrix(dR, dt, K1, K2):
    E = get_E_matrix(dR, dt)
    F = np.matmul(np.linalg.inv(K2).T, np.matmul(E,np.linalg.inv(K1)))

    return F

def get_F_matrix_from_E(E, K1, K2):
    F = np.matmul(np.linalg.inv(K2).T, np.matmul(E,np.linalg.inv(K1)))

    return F

def to_pixel_coords(K, pts):
    if len(pts.shape) == 1:
        v = np.expand_dims(v, axis=0)
    num_pts = len(pts)

    pts = np.concatenate([
        pts, np.ones((num_pts, 1))
    ], axis=-1)

    proj_pts = np.matmul(K, pts.T)[:-1,:]
    return proj_pts.T

def get_inliers_F(x1, x2, F, dist_type='symmetric', thresh=1):
    if dist_type == 'vanilla':
        epi_dist = get_epidist_w_matrix(x1, x2, F)
    elif dist_type == 'symmetric':
        epi_dist = get_episym_w_matrix(x1, x2, F)/float(2)
    else:
        print('{} is not a supported distance type'.format(dist_type))
        return
    inlier_mask = np.zeros(x1.shape[0])
    inlier_mask[epi_dist < thresh] = 1

    x1 = x1[epi_dist < thresh,:]
    x2 = x2[epi_dist < thresh,:]
    return x1, x2, inlier_mask


def get_epi_constraint(x1, x2, F):
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




# geom.py ends here
