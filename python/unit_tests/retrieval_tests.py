
import pdb
import numpy as np
import unittest

def compute_precision(desc_im1, desc_im2, dist_threshold):
	"""
	"""
	pass


def compute_recall(desc_im1, desc_im2, dist_threshold):
	"""
	"""
	pass


def get_xy_coords_from_angle(theta):
	"""
	For a unit vector, find the (x,y) positions on the unit circle, given an angle in degrees.
	"""
	x = np.cos(np.deg2rad(theta))
	y = np.sin(np.deg2rad(theta))
	return np.array([x,y])


class RetrievalUnitTests(unittest.TestCase):
	"""
		Retrieval tests
		Are they from the same image? Maybe the spatial (u,v) keypoint locations no longer matter
		Just looking at descriptors solely

		Look at HPatches Retrieval Benchmark as well
	"""
	def __init__(self):
		pass

	def test_1_unit_vectors_prec_rec(self):
		"""
		Use Euclidean distance. Imagine 2 unit vectors.
		Distance 2: np.sqrt(2) = 1.414

		Distance 1: 0.76537
		"""
		desc_1_im1 = get_xy_coords_from_angle(0)
		desc_1_im2 = get_xy_coords_from_angle(90)

		desc_2_im1 = get_xy_coords_from_angle(225)
		desc_2_im2 = get_xy_coords_from_angle(270)

		desc_1_dist = np.linalg.norm(desc_1_im1 - desc_1_im2)
		desc_2_dist = np.linalg.norm(desc_2_im1 - desc_2_im2)

		self.assertEqual(1., compute_precision(desc_im1, desc_im2, dist_threshold=1.42))
		self.assertEqual(1., compute_recall(desc_im1, desc_im2, dist_threshold=1.42))

		self.assertEqual(1/2., compute_precision(desc_im1, desc_im2, dist_threshold=1.41))
		self.assertEqual(1., compute_recall(desc_im1, desc_im2, dist_threshold=1.41))

		self.assertEqual(1., compute_precision(desc_im1, desc_im2, dist_threshold=0.77))
		self.assertEqual(1/2., compute_recall(desc_im1, desc_im2, dist_threshold=0.77))

		self.assertEqual(0., compute_precision(desc_im1, desc_im2, dist_threshold=0.76))
		self.assertEqual(0., compute_recall(desc_im1, desc_im2, dist_threshold=0.76))


	def hamming_dist_prec_rec(self):
		"""
		Hamming distance between two strings of equal length is the number of positions
		at which the corresponding symbols are different. In other words, it measures
		the minimum number of substitutions required to change one string into the other,
		or the minimum number of errors that could have transformed one string into the oth
		"""
		np.array([0,1,0,1])
		np.array([1,1,0,1])





if __name__ == '__main__':
	unittest.main()
