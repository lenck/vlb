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


    M = np.repeat(M.reshape(-1, 3, 3), num_pts, axis=0)

    x2Mx1 = np.matmul(x2.transpose(0, 2, 1), np.matmul(M, x1)).flatten()
    Mx1 = np.matmul(M, x1).reshape(-1, 3)
    Mtx2 = np.matmul(M.transpose(0, 2, 1), x2).reshape(-1, 3)

    ys = x2Mx1**2 * (
        1.0 / (Mx1[..., 0]**2 + Mx1[..., 1]**2) +
        1.0 / (Mtx2[..., 0]**2 + Mtx2[..., 1]**2))

    return ys.flatten()


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

def to_pixel_coords(K, pts):
    if len(pts.shape) == 1:
        v = np.expand_dims(v, axis=0)
    num_pts = len(pts)

    pts = np.concatenate([
        pts, np.ones((num_pts, 1))
    ], axis=-1)

    proj_pts = np.matmul(K, pts.T)[:-1,:]
    return proj_pts.T

def get_inliers_F(x1, x2, F, thresh=1):
    epi_dist = get_episym_w_matrix(x1, x2, F)

    x1 = x1[epi_dist < thresh,:]
    x2 = x2[epi_dist < thresh,:]
    return x1, x2


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
