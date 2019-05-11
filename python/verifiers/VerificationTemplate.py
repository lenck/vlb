


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

    def estimate_essential_matrix(self, pts1, pts2):
        pass

    def estimate_fundamental_matrix(self, pts1, pts2):
        pass
