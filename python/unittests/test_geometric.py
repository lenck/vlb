import unittest

import os
import sys
dirname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '{}/../'.format(dirname))

import numpy as np

import bench.geom as geom
class EpipolarGeomTests(unittest.TestCase):

    def test_epipolar_constraint(self):
        F = np.array([[1.5, 0.5, 3.0],[2.1, 1.2, 0.9],[0.8, 0.3, 0.6]])

        p = np.array([[20.3, 100.6],[134.3, 176.7],[200.1, 12.3]])


        q = np.array([[13.3, 500.2],[341.2, 54.2],[14.1, 234.3]])


        actual_constraint = np.array([ 83318.745, 126891.784, 106649.841])

        est_constraint = geom.get_epi_constraint(p, q, F)
        self.assertTrue(np.isclose(actual_constraint, est_constraint).all())

    def test_epipolar_distance(self):
        F = np.array([[1.5, 0.5, 3.0],[2.1, 1.2, 0.9],[0.8, 0.3, 0.6]])

        p = np.array([[20.3, 100.6],[134.3, 176.7],[200.1, 12.3]])


        q = np.array([[13.3, 500.2],[341.2, 54.2],[14.1, 234.3]])


        actual_distance = np.array([451.91167583, 220.64728352, 199.54633085])

        est_distance = geom.get_epidist_w_matrix(p, q, F)
        self.assertTrue(np.isclose(actual_distance, est_distance).all())
        
if __name__ == '__main__':
    unittest.main()
