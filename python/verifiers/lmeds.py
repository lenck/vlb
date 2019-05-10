
import cv2

from verifiers.VerificationTemplate import VerificationTemplate

class LMEDS(VerificationTemplate):

    def __init__(self):
        super(
            LMEDS,
            self).__init__(
                name='LMEDS',
                estimates_essential=True,
                estimates_fundamental=True)

    def evaluate_matches(self, pts1, pts2):
        _, mask = cv2.findEssentialMat(pts1, pts2, method=cv2.LMEDS)
        inlier_pts1 = pts1[mask == 1]
        inlier_pts2 = pts2[mask == 1]
        return (inlier_pts1, inlier_pts2)

    def estimate_essential_matrix(self, pts1, pts2):
        E, _ = cv2.findEssentialMat(pts1, pts2, method=cv2.LMEDS)
        return E

    def estimate_fundamental_matrix(self, pts1, pts2):
        F, _ = cv2.findFundamentalMat(pts1, pts2, method=cv2.LMEDS)
        return F
