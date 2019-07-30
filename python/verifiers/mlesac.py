"""MLESAC implementation from
https://github.com/vcg-uvic/learned-correspondence-release/blob/master/tests.py"""

import cv2
import numpy as np

from verifiers.VerificationTemplate import VerificationTemplate

MIN_PT_NUM = 8

class MLESAC(VerificationTemplate):

    def __init__(self):
        super(
            MLESAC,
            self).__init__(
                name='MLESAC',
                estimates_essential=True,
                estimates_fundamental=True)


    def estimate_essential_matrix(self, kpts1, kpts2):
        """
        Estimate the Essential matrix between 2 images from a set of putative keypoint matches
        (kpt1s[i], kpts2[i]) are a corresponding matche from image 1 and 2 in normalized coordinates

        :param kpts1: Keypoints for image 1
        :type kpts1: np.array (Nx2)
        :param kpts2: Keypoints from image 2
        :type kpts2: np.array (Nx2)
        :returns: E (the 3x3 Essential matrix)
        :rtype: np.array(3x3)
        """
        E = find_relation_matrix_mlesac(kpts1, kpts2, mat_type='essential')

        return E

    def estimate_fundamental_matrix(self, kpts1, kpts2):
        """
        Estimate the Fundamental matrix between 2 images from a set of putative keypoint matches.
        (kpt1s[i], kpts2[i]) are a corresponding matche from image 1 and 2 in camera coordinates

        :param kpts1: Keypoints for image 1
        :type kpts1: np.array (Nx2)
        :param kpts2: Keypoints from image 2
        :type kpts2: np.array (Nx2)
        :returns: E (the 3x3 Essential matrix)
        :rtype: np.array(3x3)
        """
        F = find_relation_matrix_mlesac(kpts1, kpts2, mat_type='fundamental')

        return F

def find_relation_matrix_mlesac(kpts1, kpts2, mat_type='essential', iter_num=1000,
                                thresh=0.01, probs=None, weighted=False, use_prob=False):

    """Use iterative MLESAC method to find the best reslation matrix between 2 images from a set of
     putative keypoint matches. (kpt1s[i], kpts2[i]) are a corresponding matche from image 1 and 2.

    :param kpts1: Keypoints for image 1
    :type kpts1: np.array (Nx2)
    :param kpts2: Keypoints from image 2
    :type kpts2: np.array (Nx2)
    :param thresh: threshold below which matches are considered inliers
    :type thresh: float
    :param mat_type: relation matrix to return
    :type mat_type: str ['essential' or 'fundamental']
    :param mat_type: relation matrix to return
    :type iter_num: number of iterations
    :param iter_num: int
    :param probs: probability of true match
    :type probs: np.array (N,) or None
    :param weighted: Use prob as a weight for error
    :type weighted: boolean
    :param use_prob: Use probability to weight random match choices
    :type use_prob: boolean
    :returns best_M: the relation matrix
    :rtype best_M: np.array (3x3)"""

    # Initialize 'Best' variables
    best_M = None
    best_err = np.inf

    Np = kpts1.shape[0]
    perms = np.arange(Np, dtype=np.int)

    thresh2 = thresh*thresh

    # Homogenous coordinates
    _kpts1 = np.concatenate([kpts1, np.ones((Np, 1))], axis=1)
    _kpts2 = np.concatenate([kpts2, np.ones((Np, 1))], axis=1)


    for n in range(iter_num):
        # Randomly select depending on the probability (if given)
        if probs is not None:
            probs /= np.sum(probs)
        if use_prob:
            cur_subs = np.random.choice(
                perms, MIN_PT_NUM, replace=False, p=probs)
        else:
            cur_subs = np.random.choice(
                perms, MIN_PT_NUM, replace=False, p=None)

        sub_kpts1 = kpts1[cur_subs, :]
        sub_kpts2 = kpts2[cur_subs, :]
        if mat_type=='essential':
            Ms, mask = cv2.findEssentialMat(
                sub_kpts1, sub_kpts2, focal=1, pp=(0, 0), method=cv2.RANSAC)
        elif mat_type=='fundamental':
            Ms, mask = cv2.findFundamentalMat(
                sub_kpts1, sub_kpts2, focal=1, pp=(0, 0), method=cv2.RANSAC)
        else:
            print("Incorrect matrix type selected")
            return

        if Ms is None:
            continue

        for i in range(0, Ms.shape[0], 3):
            M = Ms[i:i + 3, :]
            err = compute_error(_kpts1, _kpts2, M)

            inliers = err <= thresh2

            if weighted:
                sum_err = (np.abs(err) * probs).sum()
            else:
                sum_err = np.abs(err).sum()

        if sum_err < best_err:
            best_err = sum_err
            best_M = M

    return best_M

def compute_error(x1, x2, E):
    """
    Compute the symmetric epipolar distance error for sets of putative matches

    :param x1: Keypoints for image 1
    :type x1: np.array (Nx2)
    :param x2: Keypoints from image 2
    :type x2: np.array (Nx2)
    :param M: the relation matrix
    :rtype M: np.array (3x3)
    :param err: Epipolar Symmetirc error for each putative match
    :rtype err: np.array (N,)"""

    Ex1 = E.dot(x1.T)
    Etx2 = E.T.dot(x2.T)

    Ex1 = E.dot(x1.T)
    Etx2 = E.T.dot(x2.T)
    x2tEx1 = np.sum(x2.T * Ex1, axis=0)

    a = Ex1[0] * Ex1[0]
    b = Ex1[1] * Ex1[1]
    c = Etx2[0] * Etx2[0]
    d = Etx2[1] * Etx2[1]

    err = x2tEx1 * x2tEx1 / (a + b + c + d)

    return err
