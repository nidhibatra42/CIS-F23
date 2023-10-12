import numpy as np
import pivotCalibration

def test_calibration(self):
        # Define known transformation parameters (rotation matrix and pivot point)
        R_i = np.array([[0.866, -0.5, 0], [0.5, 0.866, 0], [0, 0, 1]])
        p_i = np.array([1.0, 2.0, 3.0])

        # Generate a set of points to transform using R_i and p_i
        points = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

        # Apply the transformation to the points
        transformed_points = np.dot(R_i, points.T).T + p_i

        # Call your pivot_calibration function to estimate the unknown translation
        estimated_translation = pivotCalibration.pivot_calibration(points, transformed_points)

        # Define the ground truth translation
        ground_truth_translation = p_i

        # Check if the estimated translation matches the ground truth
        np.testing.assert_array_almost_equal(estimated_translation, ground_truth_translation, decimal=2)