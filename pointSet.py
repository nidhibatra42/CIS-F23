import numpy as np
import meanPoint

class PointSet:
    """A class to perform point set registration
    """

    def __init__(self, points):
        """Initialize a PointSet object with a set of 3D points.

        Args:
            points (numpy.ndarray): An array of 3D points.
        """     

        self.points = points

    def find_registration(self, b):
        """Find the rotation matrix and translation vector for registering
        the current point set onto a new point set 'b'.

        Args:
            b (PointSet): Another PointSet object to register with.

        Returns:
            R (numpy.ndarray): The rotation matrix.
            p (numpy.ndarray): The translation vector.
        """
    
        #Calculate H
        H = np.empty((3, 3))

        a_tilde = self.points - np.mean(self.points, axis=0)
        b_tilde = b.points - np.mean(b.points, axis=0)
        
        for i in range(0, min(len(self.points), len(b.points))):
            H += np.matrix([
                [a_tilde[i][0] * b_tilde[i][0], a_tilde[i][0] * b_tilde[i][1], a_tilde[i][0] * b_tilde[i][2]],
                [a_tilde[i][1] * b_tilde[i][0], a_tilde[i][1] * b_tilde[i][1], a_tilde[i][1] * b_tilde[i][2]],
                [a_tilde[i][2] * b_tilde[i][0], a_tilde[i][2] * b_tilde[i][1], a_tilde[i][2] * b_tilde[i][2]]
                ])
        

        #Find SVD of H
        U, S, Vt = np.linalg.svd(H)

        #Calculate R
        Ut = U.transpose()
        V = Vt.transpose()
        R = np.dot(V, Ut)

        R = self.check_rot_algorithm(R, Ut, V)
        p = self.find_translation(R, b)

        return R, p

    def check_rot_algorithm(self, R, Ut, V):
        """Ensure that the determinant of R is 1, or negate the last term of V to fix it.
        Note: This algorithm works for the noiseless case.

        Args:
            R (numpy.ndarray): The rotation matrix.
            Ut (numpy.ndarray): The transpose of the left singular vector.
            V (numpy.ndarray): The right singular vector.

        Returns:
            R (numpy.ndarray): The corrected rotation matrix.
        """
        
        #Check determinant
        if self.is_almost_one(np.linalg.det(R)):
            return R
        
        #Negate last value if necessary
        for frame in V:
            frame[2] = -frame[2]

        return np.dot(V, Ut)
    
    
    def find_translation(self, R, b):
        """Find p between self and other point cloud, given R"""
        a_bar = meanPoint.mean_point(self.points)
        b_bar = meanPoint.mean_point(b.points)

        return b_bar - np.dot(R, a_bar)
    
    
    def is_almost_one(self, det):
        """Check if the determinant of a matrix is almost equal to 1.

        Args:
            det (float): The determinant value to check.

        Returns:
            bool: True if the determinant is almost 1, False otherwise.
        """      
        return abs(det - 1) <= 1e-9
    
