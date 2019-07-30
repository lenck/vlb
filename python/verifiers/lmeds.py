
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

    def estimate_essential_matrix(self, pts1, pts2):
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
        E, _ = cv2.findEssentialMat(pts1, pts2, method=cv2.LMEDS)
        return E

    def estimate_fundamental_matrix(self, pts1, pts2):
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
        F, _ = cv2.findFundamentalMat(pts1, pts2, method=cv2.LMEDS)
        return F
