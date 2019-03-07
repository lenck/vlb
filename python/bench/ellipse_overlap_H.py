#!/usr/bin/python
# -*- coding: utf-8 -*-
# ===========================================================
#  File Name: ellipse_overlap_H.py
#  Author: Xu Zhang, Columbia University
#  Creation Date: 01-25-2019
#  Last Modified: Tue Mar  5 00:02:37 2019
#
#  Usage: python ellipse_overlap_H.py
#  Description:
#
#  Copyright (C) 2018 Xu Zhang
#  All rights reserved.
#
#  This file is made available under
#  the terms of the BSD license (see the COPYING file).
# ===========================================================

from bench.parse_arg import parse_arg
import numpy as np
import copy
import scipy.spatial.distance
import scipy.io as sio

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})

import bench.vlb_greedy_matching
import bench.vgg_compute_ellipse_overlap


def frame2ellipse(fa):
    if fa is None or fa.shape[0] == 0:
        return []
    assert (fa.shape[1] >= 2 and fa.shape[1] <= 6), 'Invalid feature length'

    ellipses = np.zeros([fa.shape[0], 5])
    if fa.shape[1] == 2:
        ellipses[:, 0:2] = fa[:, 0:2]
        ellipses[:, 2] = 1
        ellipses[:, 4] = 1
    elif (fa.shape[1] == 3 or fa.shape[1] == 4):
        ellipses[:, 0:2] = fa[:, 0:2]
        ellipses[:, 2] = fa[:, 2]**2
        ellipses[:, 4] = fa[:, 2]**2
    elif fa.shape[1] == 5:
        ellipses = copy.copy(fa)
    else:
        ellipses[:, 0:2] = fa[:, 0:2]
        for k in range(fa.shape[0]):
            A = np.reshape(fa[k, 2:6], (2, 2))
            E = np.matmul(A.transpose(), A)
            ellipses[k, 2] = E[0, 0]
            ellipses[k, 3] = E[0, 1]
            ellipses[k, 4] = E[1, 1]
    return ellipses


def ellipse_warp(H, ell_o, method):
    ell = copy.copy(ell_o)
    ell[:, 0:2] = ell[:, 0:2] - 1
    well = np.zeros(ell.shape, dtype=np.double)

    for i in range(ell.shape[0]):
        if method == 'standard':
            S = np.array([[ell[i, 2], ell[i, 3], 0], [
                         ell[i, 3], ell[i, 4], 0], [0, 0, -1]])
            T = np.array([[1, 0, ell[i, 0]], [0, 1, ell[i, 1]], [0, 0, 1]])

            M = np.matmul(
                np.matmul(
                    np.matmul(
                        np.matmul(
                            H,
                            T),
                        S),
                    T.transpose()),
                H.transpose())
            M = -M / M[2, 2]
            t_ = -M[0:2, [2]]
            S_ = M[0:2, 0:2] + np.matmul(t_, t_.transpose())
            well[i, 0:2] = t_[:, 0]
            well[i, 2:5] = np.array([S_[0, 0], S_[0, 1], S_[1, 1]])

        elif method == 'linearise':
            Mi1 = [[ell[i, 2], ell[i, 3]], [ell[i, 3], ell[i, 4]]]
            x = ell[i, 0]
            y = ell[i, 1]
            h11 = H[0, 0]
            h12 = H[0, 1]
            h13 = H[0, 2]
            h21 = H[1, 0]
            h22 = H[1, 1]
            h23 = H[1, 2]
            h31 = H[2, 0]
            h32 = H[2, 1]
            h33 = H[2, 2]
            fxdx = h11 / (h31 * x + h32 * y + h33) - (h11 * x +
                                                      h12 * y + h13) * h31 / (h31 * x + h32 * y + h33)**2
            fxdy = h12 / (h31 * x + h32 * y + h33) - (h11 * x +
                                                      h12 * y + h13) * h32 / (h31 * x + h32 * y + h33)**2
            fydx = h21 / (h31 * x + h32 * y + h33) - (h21 * x +
                                                      h22 * y + h23) * h31 / (h31 * x + h32 * y + h33)**2
            fydy = h22 / (h31 * x + h32 * y + h33) - (h21 * x +
                                                      h22 * y + h23) * h32 / (h31 * x + h32 * y + h33)**2
            Aff = np.array([[fxdx, fxdy], [fydx, fydy]])

            l1 = [ell[i, 0], ell[i, 1], 1]
            l1_2 = np.matmul(H, l1)
            l1_2 = l1_2 / l1_2[2]
            well[i, 0] = l1_2[0]
            well[i, 1] = l1_2[1]
            BMB = np.matmul(np.matmul(Aff, Mi1), Aff.transpose())
            well[i, 2:5] = [BMB[0, 0], BMB[0, 1], BMB[1, 1]]

    well[:, 0:2] = well[:, 0:2] + 1
    return well


def ellipse_in_bbox(f, bbox):
    assert len(bbox) == 4, 'Invalid bounding box'
    assert f.shape[1] == 5, 'Invalid ellipse frames.'

    if f.shape[0] == 0:
        return False

    rx = np.sqrt(f[:, 2])
    ry = np.sqrt(f[:, 4])

    sel = (f[:, 0] - rx) > bbox[0]
    sel = np.logical_and(sel, ((f[:, 1] - ry) > bbox[1]))
    sel = np.logical_and(sel, ((f[:, 0] + rx) < bbox[2]))
    sel = np.logical_and(sel, ((f[:, 1] + ry) < bbox[3]))
    return sel


def ellipse_eigen(frames):
    numFrames = frames.shape[0]
    eigval = np.zeros((numFrames, 2), dtype=np.double)
    eigvec = np.zeros((numFrames, 4), dtype=np.double)

    for i in range(numFrames):
        matrix = np.zeros((2, 2), dtype=np.double)
        matrix[0, 0] = frames[i, 2]
        matrix[0, 1] = frames[i, 3]
        matrix[1, 0] = frames[i, 3]
        matrix[1, 1] = frames[i, 4]
        evals, evecs = np.linalg.eig(matrix)
        eigvec[i, :] = np.array(
            [evecs[0, 0], evecs[1, 0], evecs[0, 1], evecs[1, 1]])
        eigval[i, :] = np.array([evals[0], evals[1]])

    return eigval, eigvec


def ellipse2vggformat(ell, eigVal, eigVec):

    vggEll = np.zeros((ell.shape[0], 5 + 4), dtype=np.double)

    if ell.shape[0] == 0:
        return vggEll

    vggEll[:, 0:2] = ell[:, 0:2]
    v1byLambda1 = eigVec[:, 0:2] / \
        np.repeat(np.finfo(float).eps + eigVal[:, [0]], 2, axis=1)
    v2byLambda2 = eigVec[:, 2:4] / \
        np.repeat(np.finfo(float).eps + eigVal[:, [1]], 2, axis=1)

    A1 = np.sum(np.hstack((v1byLambda1[:, [0]], v2byLambda2[:, [
                0]])) * np.hstack((eigVec[:, [0]], eigVec[:, [2]])), axis=1)
    A2 = np.sum(np.hstack((v1byLambda1[:, [1]], v2byLambda2[:, [
                1]])) * np.hstack((eigVec[:, [0]], eigVec[:, [2]])), axis=1)
    A4 = np.sum(np.hstack((v1byLambda1[:, [1]], v2byLambda2[:, [
                1]])) * np.hstack((eigVec[:, [1]], eigVec[:, [3]])), axis=1)

    vggEll[:, 2] = A1
    vggEll[:, 3] = A2
    vggEll[:, 4] = A4

    vggEll[:, 5] = np.sqrt(eigVal[:, 1])
    vggEll[:, 6] = np.sqrt(eigVal[:, 0])

    vggEll[:, 7] = np.sqrt(ell[:, 2])
    vggEll[:, 8] = np.sqrt(ell[:, 4])

    return vggEll


def ellipse_overlap_fast(f1, f2, options):
    opts = {}
    opts['normaliseFrames'] = True
    opts['normalisedScale'] = 30
    opts['minAreaRatio'] = 0.3
    opts['frame2frame'] = False
    opts['fix'] = False
    parse_arg(opts, options)

    N2 = f2.shape[0]

    ellipsePairs = []
    scores = []

    if f1.shape[0] == 0 or f2.shape[0] == 0:
        return ellipsePairs, scores

    f1 = frame2ellipse(f1)
    f2 = frame2ellipse(f2)

    e1, eigVec1 = ellipse_eigen(f1)
    e2, eigVec2 = ellipse_eigen(f2)

    vggEll1 = ellipse2vggformat(f1, e1, eigVec1)
    vggEll2 = ellipse2vggformat(f2, e2, eigVec2)

    a1 = np.pi * np.sqrt(np.prod(e1, axis=1))
    a2 = np.pi * np.sqrt(np.prod(e2, axis=1))

    for i2 in range(N2):
        if opts['normaliseFrames']:
            s = opts['normalisedScale'] / np.sqrt(a2[i2] / np.pi)
        else:
            s = 1

        if opts['frame2frame']:
            ellipsePairs[i2] = np.hstack[i2 *
                                         np.ones((f1.shape[0], 1), dtype=np.int), np.xrange(f1.shape[0])]
        else:
            thr = 4 * np.sqrt(a2[i2] / np.pi)
            if opts['fix']:
                thr = thr * s
            canOverlap = scipy.spatial.distance.cdist(
                f2[[i2], 0:2], f1[:, 0:2], 'euclidean') < thr
            maxOverlap = np.minimum(a2[i2], a1) / \
                np.maximum(a2[i2], a1) * canOverlap
            _, pairs = np.where(maxOverlap > opts['minAreaRatio'])
            ellipsePairs.extend(zip([i2] * pairs.shape[0], pairs.tolist()))
        if len(pairs) == 0:
            continue

        if opts['normaliseFrames']:
            vggS = np.array([1, 1, 1 / s**2, 1 / s**2, 1 / s**2, s, s, s, s])
            lhsEllipse = vggS * vggEll2[[i2]]
            rhsEllipse = vggEll1[pairs] * vggS
        else:
            lhsEllipse = vggEll2[[i2]]
            rhsEllipse = vggEll1[pairs]
        _, tw, _, _ = bench.vgg_compute_ellipse_overlap.vgg_compute_ellipse_overlap(
            lhsEllipse, rhsEllipse, -1)
        scores.extend((1 - tw / 100).tolist()[0])
    return np.array(ellipsePairs), np.array(scores)


def ellipse_overlap_H(geom, fa, fb, options):
    opts = {}
    opts['mode'] = 'frames'
    parse_arg(opts, options)

    if opts['mode'] == 'descriptors':
        opts['normaliseFrames'] = False
        opts['maxOverlapError'] = 0.5
        opts['cropFrames'] = False
    else:
        opts['normaliseFrames'] = True
        opts['maxOverlapError'] = 0.4
        opts['cropFrames'] = True

    opts['normalisedScale'] = 30
    opts['magnification'] = 3
    opts['warpMethod'] = 'linearise'
    opts['cropFramesSafetyEdge'] = []
    parse_arg(opts, options)

    info = {}
    tcorr = []
    corr_score = []
    overlapThresh = 1 - opts['maxOverlapError']

    ella = frame2ellipse(fa)
    ellb = frame2ellipse(fb)

    ella_rep = ellipse_warp(geom['H'], ella, opts['warpMethod'])
    ellb_rep = ellipse_warp(np.linalg.inv(geom['H']), ellb, opts['warpMethod'])

    fa_valid = np.array([True] * fa.shape[0])
    fb_valid = np.array([True] * fa.shape[1])
    if opts['cropFrames']:
        bba = np.array([1, 1, geom['ima_size'][1] +
                        1, geom['ima_size'][0] + 1])
        bbb = np.array([1, 1, geom['imb_size'][1] +
                        1, geom['imb_size'][0] + 1])
        if opts['cropFramesSafetyEdge']:
            ser = opts['cropFramesSafetyEdge']
            bba = bba + np.array([geom['refimsize'] *
                                  ser, -geom['refimsize'] * ser])
            bbb = bbb + np.array([geom['imsize'] * ser, -geom['imsize'] * ser])
        fa_valid = np.logical_and(
            ellipse_in_bbox(
                ella, bba), ellipse_in_bbox(
                ella_rep, bbb))
        fb_valid = np.logical_and(
            ellipse_in_bbox(
                ellb_rep, bba), ellipse_in_bbox(
                ellb, bbb))

    info['fa_valid'] = fa_valid
    info['fb_valid'] = fb_valid

    info['ella'] = ella[fa_valid, :]
    info['ellb'] = ellb[fb_valid, :]
    info['ella_rep'] = ella_rep[fa_valid, :]
    info['ellb_rep'] = ellb_rep[fb_valid, :]
    if np.sum(fa_valid) == 0 or np.sum(fb_valid) == 0:
        return tcorr, corr_score, info

    if info['ella'].shape[0] == 0 or info['ellb'].shape[0] == 0:
        return tcorr, corr_score, info

    if not opts['normaliseFrames']:
        magFactor = opts['magnification']**2
        ella[:, 2:5] = ella[:, 2:5] * magFactor
        ellb_rep = ellb_rep[:, 2:5] * magFactor

    matching_option = {}
    matching_option['normaliseFrames'] = opts['normaliseFrames']
    matching_option['minAreaRatio'] = overlapThresh
    matching_option['normalisedScale'] = opts['normalisedScale']
    parse_arg(matching_option, options)

    ellipsesPairs, ellipsesOverlaps = ellipse_overlap_fast(
        ellb_rep[fb_valid, :], ella[fa_valid, :], matching_option)
    isValid = ellipsesOverlaps > overlapThresh
    tcorr = ellipsesPairs[isValid]
    corr_score = ellipsesOverlaps[isValid]
    return tcorr, corr_score, info


def match_greedy(data, qdata):
    dists = scipy.spatial.distance.cdist(data, qdata, 'sqeuclidean')
    dists = dists.reshape((data.shape[0] * qdata.shape[0],))
    data_ind = np.repeat(
        np.arange(
            data.shape[0]).reshape(
            (data.shape[0], 1)), qdata.shape[0], axis=1)
    data_ind = data_ind.reshape((data.shape[0] * qdata.shape[0], 1))
    qdata_ind = np.repeat(
        np.arange(
            qdata.shape[0]).reshape(
            (qdata.shape[0], 1)), data.shape[0], axis=1)
    qdata_ind = np.transpose(qdata_ind)
    qdata_ind = qdata_ind.reshape((data.shape[0] * qdata.shape[0], 1))
    ind_matrix = np.hstack((data_ind, qdata_ind))
    perm_index = np.argsort(dists, kind='mergesort')

    dists = dists[perm_index]
    ind_matrix = ind_matrix[perm_index, :]

    matches, _ = bench.vlb_greedy_matching.vlb_greedy_matching(
        data.shape[0], qdata.shape[0], ind_matrix)
    matches = matches[:, 0]
    matches = matches.reshape((data.shape[0], 1))
    matches = np.hstack(
        (np.arange(
            data.shape[0]).reshape(
            (data.shape[0], 1)), matches))
    matches = matches[matches[:, 1] > -1, :]

    return matches


def main():
    data = sio.loadmat('data.mat')
    #feature_1 = np.array([[14.8277397,5.3841510e+02,2.0014350,4.4456816]])
    #feature_2 = np.array([[40.2015991,5.2250775e+02,2.3041577,4.4541903]])
    feature_1 = np.array(
        [[14.8277397, 5.3841510e+02, 2.0014350, 4.4456816]], dtype=np.float32)
    feature_2 = np.array(
        [[40.2015991, 5.2250775e+02, 2.3041577, 4.4541903]], dtype=np.float32)

    #feature = np.array([[1,3,4,1,4,7],[2,4,5,2,5,8],[5,6,6,3,6,9]])
    #feature2 = np.array([[1,3,4,1,4,7],[2,4,5,2,5,8],[5,6,6,3,6,9]])
    #feature = np.array([[100,200,4,1,4,7],[101,201,5,2,5,8],[300,400,6,3,6,9]])
    #feature2 = np.array([[100,200,4,1,4,7],[200,300,5,2,5,8],[300,400,6,3,6,9]])
    # print(frame2ellipse(feature))
    #ellipse = frame2ellipse(feature)
    # print(ellipse)
    #H = np.array([[0.8,0.7,5],[0.6,0.9,10],[0,0,1]])
    #H1 = np.eye(3)
    geom = {}
    geom['H'] = data['geom']['H'][0][0]
    geom['ima_size'] = (1000, 1000)
    geom['imb_size'] = (1000, 1000)
    geom['refimsize'] = (1000, 1000)
    geom['imsize'] = (1000, 1000)
    #new_ellipse = ellipse_warp(H, ellipse, 'standard')
    #data['geom']['H'] = data['geom']['H'][0][0]
    # print(data['geom']['H'][0][0])
    tcorr, corr_score, info = ellipse_overlap_H(
        geom, feature_1, feature_2, {'maxOverlapError': 0.5})
    print(tcorr, corr_score)
