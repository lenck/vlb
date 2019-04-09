import unittest


import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '{}/../'.format(dir_path))

import bench.Utils
import bench.MatchingScoreBench

import numpy as np

class TestMetrics(unittest.TestCase):

    def test_repeatability(self):
        pass

    def test_matching_100_perc_with_equal_features_descriptors_and_matchGeometry(self):
        ms_bench = bench.MatchingScoreBench.MatchingScoreBench(matchGeometry=True)

        # Define instance variable set by wrapper method
        ms_bench.norm_factor = 'minab'

        feature_1 = np.array([[29, 31],[93, 26],[33, 52],[82, 73]])

        descriptor_1 = np.array([[3, 1, 0, 3, 0, 1, 3, 0, 1, 0],
                                 [2, 1, 0, 1, 1, 2, 2, 3, 0, 2],
                                 [2, 1, 0, 3, 2, 1, 1, 3, 3, 0],
                                 [3, 3, 2, 3, 1, 3, 2, 3, 1, 2]])


        input_1 = [feature_1,descriptor_1]
        input_2 = [feature_1,descriptor_1]

        geom = {}
        geom['H'] = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])

        geom['refimsize'] = [100,100]
        geom['ima_size'] = [100,100]
        geom['imb_size'] = [100,100]

        _, _, ms, num_matches = ms_bench.evaluate_unit(input_1,input_2, geom)

        self.assertEqual(ms, 1.0)
        self.assertEqual(num_matches, 4.0)

    def test_matching_100_perc_with_equal_features_descriptors_notGeoMatch(self):
        ms_bench = bench.MatchingScoreBench.MatchingScoreBench(matchGeometry=False)

        # Define instance variable set by wrapper method
        ms_bench.norm_factor = 'minab'

        feature_1 = np.array([[29, 31],[93, 26],[33, 52],[82, 73]])

        descriptor_1 = np.array([[3, 1, 0, 3, 0, 1, 3, 0, 1, 0],
                                 [2, 1, 0, 1, 1, 2, 2, 3, 0, 2],
                                 [2, 1, 0, 3, 2, 1, 1, 3, 3, 0],
                                 [3, 3, 2, 3, 1, 3, 2, 3, 1, 2]])


        input_1 = [feature_1,descriptor_1]
        input_2 = [feature_1,descriptor_1]

        geom = {}
        geom['H'] = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])

        geom['refimsize'] = [100,100]
        geom['ima_size'] = [100,100]
        geom['imb_size'] = [100,100]

        _, _, ms, num_matches = ms_bench.evaluate_unit(input_1,input_2, geom)

        self.assertEqual(ms, 1.0)
        self.assertEqual(num_matches, 4.0)

    def test_matching_50_perc_matchGeometry(self):
        ms_bench = bench.MatchingScoreBench.MatchingScoreBench(matchGeometry=True)

        # Define instance variable set by wrapper method
        ms_bench.norm_factor = 'minab'

        feature_1 = np.array([[29, 31],[93, 26]])
        feature_2 = np.array([[29, 31],[10, 20]])

        descriptor_1 = np.array([[3, 1, 0, 3, 0, 1, 3, 0, 1, 0],
                                 [2, 1, 0, 1, 1, 2, 2, 3, 0, 2]])

        descriptor_2 = np.array([[3, 1, 0, 3, 0, 1, 3, 0, 1, 0],
                                 [2, 1, 0, 1, 1, 2, 2, 3, 0, 2]])


        input_1 = [feature_1,descriptor_1]
        input_2 = [feature_2,descriptor_2]

        geom = {}
        geom['H'] = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])

        geom['refimsize'] = (100,100)
        geom['ima_size'] = (100,100)
        geom['imb_size'] = (100,100)

        _, _, ms, num_matches = ms_bench.evaluate_unit(input_1,input_2, geom)

        self.assertEqual(ms, 0.5)
        self.assertEqual(num_matches, 1.0)

    def test_matching_50_perc_nonMatchGeometry(self):
        ms_bench = bench.MatchingScoreBench.MatchingScoreBench(matchGeometry=False)

        # Define instance variable set by wrapper method
        ms_bench.norm_factor = 'minab'

        feature_1 = np.array([[29, 31],[93, 26]])
        feature_2 = np.array([[29, 31],[10, 20]])

        descriptor_1 = np.array([[3, 1, 0, 3, 0, 1, 3, 0, 1, 0],
                                 [2, 1, 0, 1, 1, 2, 2, 3, 0, 2]])


        input_1 = [feature_1,descriptor_1]
        input_2 = [feature_2,descriptor_1]

        geom = {}
        geom['H'] = np.array([[1.0,0,0],[0,1.0,0],[0,0,1.0]])

        geom['refimsize'] = (100,100)
        geom['ima_size'] = (100,100)
        geom['imb_size'] = (100,100)

        _, _, ms, num_matches = ms_bench.evaluate_unit(input_1,input_2, geom)

        self.assertEqual(ms, 0.5)
        self.assertEqual(num_matches, 1.0)

    def test_geometric_verification(self):
        pass

if __name__ == "__main__":
    unittest.main()
