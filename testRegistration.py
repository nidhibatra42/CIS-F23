import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
import unittest

class RegistrationTest(unittest.TestCase):
    def test_registration(self):
        # Generate a random 3D point cloud with 100 points
        num_points = 100
        source_cloud = np.random.rand(num_points, 3) * 10  # Random points between 0 and 10
        source_cloud_set = PointSet(source_cloud)

        #  Apply a known transformation (e.g., translation and rotation) to create the target cloud
        translation_vector = np.array([1.0, 2.0, 0.5])
        rotation_matrix = np.array([[0.866, -0.5, 0.0], [0.5, 0.866, 0.0], [0.0, 0.0, 1.0]])  # 30-degree rotation around z-axis

        target_cloud = np.dot(source_cloud, rotation_matrix.T) + translation_vector
        target_cloud_set = PointSet(target_cloud)


        # Calculate and compare the transformation parameters with the known transformation.
        Rnew, pnew = source_cloud_set.find_registration(target_cloud_set)

        matrix_calculated = transform_from(Rnew, pnew)
        matrix_expected = transform_from(rotation_matrix, translation_vector)

        self.assertEquals(matrix_calculated, matrix_expected)

if __name__ == "__main__":
    unittest.main()