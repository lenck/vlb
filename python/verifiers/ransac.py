
import cv2

from verifiers.VerificationTemplate import VerificationTemplate

class RANSAC(VerificationTemplate):

    def __init__(self):
        super(
            RANSAC,
            self).__init__(
                name='RANSAC',
                estimates_essential=True,
                estimates_fundamental=True)

    def evaluate_matches(self, pts1, pts2):
        _, mask = cv2.findEssentialMat(pts1, pts2, method=cv2.RANSAC)
        inlier_pts1 = pts1[mask.ravel() == 1]
        inlier_pts2 = pts2[mask.ravel() == 1]
        return (inlier_pts1, inlier_pts2)

    def estimate_essential_matrix(self, pts1, pts2):
        E, _ = cv2.findEssentialMat(pts1, pts2, method=cv2.RANSAC)
        return E

    def estimate_fundamental_matrix(self, pts1, pts2):
        F, _ = cv2.findFundamentalMat(pts1, pts2, method=cv2.RANSAC)
        return F
