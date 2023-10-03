import numpy as np

class PointSetRegistration:


    def __init__(self, points):
        """Initialize a point set with a 2d list of points.
            Each point should have a list with the x, y, z coors.
            """
        self.points = points

    def find_registration(self, b):
        """Find R value for point set registration for class object
            onto new point set b

            TODO: error case if a and b don't have the same number of points
            """
        #Calculate H
        H = np.empty((3, 3))

        a_tilde = self.points - np.mean(self.points)
        b_tilde = b.points - np.mean(b.points)
        
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
        """Confirm that determinant of R is 1,
            or negate the last term of V to fix it
            Note: this algorithm works for noiseless case
        """
        #Check determinant
        if np.det(R) == 1:
            return R
        
        #Negate last value if necessary
        V[2] = -1 * V[2]
        return np.dot(V, Ut)
    
    def find_translation(self, R, b):
        """Find p between self and other point cloud, given R"""
        return np.mean(b) - np.dot(R, np.mean(self.points))
    
