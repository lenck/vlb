"""MLESAC implementation from
https://github.com/vcg-uvic/learned-correspondence-release/blob/master/tests.py"""
import cv2
import numpy as np

from verifiers.VerificationTemplate import VerificationTemplate
class MLESAC(VerificationTemplate):

    def __init__(self):
        super(
            MLESAC,
            self).__init__(
                name='MLESAC',
                estimates_essential=True,
                estimates_fundamental=True)


    def estimate_essential_matrix(self, np1, np2):
        iter_num=1000
        threshold=0.01
        probs=None
        weighted=False
        use_prob=False

        min_pt_num = 5
        Np = np1.shape[0]
        perms = np.arange(Np, dtype=np.int)

        best_E = None
        best_inliers = None
        best_err = np.inf

        _np1 = np.concatenate([np1, np.ones((Np, 1))], axis=1)
        _np2 = np.concatenate([np2, np.ones((Np, 1))], axis=1)

        thresh2 = threshold * threshold

        for n in range(iter_num):
            # Randomly select depending on the probability (if given)
            if probs is not None:
                probs /= np.sum(probs)
            if use_prob:
                cur_subs = np.random.choice(
                    perms, min_pt_num, replace=False, p=probs)
            else:
                cur_subs = np.random.choice(
                    perms, min_pt_num, replace=False, p=None)

            sub_np1 = np1[cur_subs, :]
            sub_np2 = np2[cur_subs, :]
            Es, mask = cv2.findEssentialMat(
                sub_np1, sub_np2, focal=1, pp=(0, 0), method=cv2.RANSAC)
            if Es is None:

                continue

            for i in range(0, Es.shape[0], 3):
                E = Es[i:i + 3, :]
                err = compute_error(_np1, _np2, E)

                inliers = err <= thresh2

                if weighted:
                    sum_err = (np.abs(err) * probs).sum()
                else:
                    sum_err = np.abs(err).sum()
            if sum_err < best_err:
                best_err = sum_err
                best_E = E
                best_inliers = inliers

        best_inliers = best_inliers.reshape(-1, 1).astype(np.uint8)

        return best_E

    def estimate_fundamental_matrix(self, np1, np2):
        iter_num=1000
        threshold=0.01
        probs=None
        weighted=False
        use_prob=False

        min_pt_num = 8
        Np = np1.shape[0]
        perms = np.arange(Np, dtype=np.int)

        best_F = None
        best_inliers = None
        best_err = np.inf

        _np1 = np.concatenate([np1, np.ones((Np, 1))], axis=1)
        _np2 = np.concatenate([np2, np.ones((Np, 1))], axis=1)

        thresh2 = threshold * threshold

        for n in range(iter_num):
            # Randomly select depending on the probability (if given)
            if probs is not None:
                probs /= np.sum(probs)
            if use_prob:
                cur_subs = np.random.choice(
                    perms, min_pt_num, replace=False, p=probs)
            else:
                cur_subs = np.random.choice(
                    perms, min_pt_num, replace=False, p=None)

            sub_np1 = np1[cur_subs, :]
            sub_np2 = np2[cur_subs, :]
            Fs, mask = cv2.findFundamentalMat(
                sub_np1, sub_np2, method=cv2.RANSAC)
            if Fs is None:

                continue

            for i in range(0, Fs.shape[0], 3):
                F = Fs[i:i + 3, :]
                err = compute_error(_np1, _np2, F)

                inliers = err <= thresh2

                if weighted:
                    sum_err = (np.abs(err) * probs).sum()
                else:
                    sum_err = np.abs(err).sum()
            if sum_err < best_err:
                best_err = sum_err
                best_F = F
                best_inliers = inliers

        best_inliers = best_inliers.reshape(-1, 1).astype(np.uint8)

        return best_F

def compute_error(x1, x2, E):
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
