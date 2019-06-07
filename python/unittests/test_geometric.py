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

        est_distance = geom.get_epidist(p, q, F, type='vanilla')
        self.assertTrue(np.isclose(actual_distance, est_distance).all())


    def test_epipolar_symmetric_distance(self):
        F = np.array([[1.5, 0.5, 3.0],[2.1, 1.2, 0.9],[0.8, 0.3, 0.6]])

        p = np.array([[20.3, 100.6],[134.3, 176.7],[200.1, 12.3]])


        q = np.array([[13.3, 500.2],[341.2, 54.2],[14.1, 234.3]])


        actual_distance = np.array([519.57930546, 410.21340087, 380.48729151])

        est_distance = geom.get_epidist(p, q, F,  type='symmetric')

        self.assertTrue(np.isclose(actual_distance, est_distance).all())


    def test_get_F_from_E(self):
        K1 = np.array([[8.0, 0, 0],[0, 8.0, 0],[0, 0, 1.0]])
        K2 = np.array([[10.0, 0, 0],[0, 10.0, 0],[0, 0, 1.0]])

        E = np.array([[ 0.0150983 ,  0.80463425, -0.06742306],
                      [-0.93076557,  0.00397582,  0.36069718],
                      [ 0.05787116, -0.58947824,  0.02265874]])


        actual_F = np.array([[ 1.88728728e-04,  1.00579281e-02, -6.74230601e-03],
                            [-1.16345697e-02,  4.96978089e-05,  3.60697176e-02],
                            [ 7.23389441e-03, -7.36847802e-02,  2.26587430e-02]])

        est_F = geom.get_F_matrix_from_E(E, K1, K2)

        self.assertTrue(np.isclose(actual_F, est_F).all())

    def test_get_precision_recall(self):
        true_class = np.array([1,0,0,1,1])
        predicted_class = np.array([0,1,0,1,1])

        tp = 2.0
        tn = 1.0
        fp = 1.0
        fn = 1.0

        true_precision = tp/(tp + fp)
        true_recall = tp/(tp + fn)

        precision, recall = geom.get_pr_recall(true_class, predicted_class)

        self.assertAlmostEqual(true_precision, precision)
        self.assertAlmostEqual(true_recall, recall)

if __name__ == '__main__':
    unittest.main()
