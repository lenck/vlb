


class VerificationTemplate():
    """Basic Template for Verification Algorithm

    Attributes
    ----------

    name: str
        Name of the method
    estimates_essential: boolean, optional
        Does the algorithm estimate the essential matrix
    estimates_fundamental: boolean, optional
        Does the algorithm estimate the fundamental matrix

    """

    def __init__(self, name, estimates_essential=False, estimates_fundamental=False):

        self.name = name
        self.estimates_essential = estimates_essential
        self.estimates_fundamental = estimates_fundamental

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
        pass

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
        pass
