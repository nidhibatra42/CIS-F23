import numpy as np

class PointSet:
    """_summary_
    """

    def __init__(self, points):
        """_summary_

        Args:
            points (_type_): _description_
        """        

        self.points = points

    def find_registration(self, b):
        """Find R value for point set registration for class object
            onto new point set b

        Args:
            b (_type_): _description_

        Returns:
            _type_: _description_
            TODO: error case if a and b don't have the same number of points
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
        """_summary_

        Args:
            R (_type_): _description_
            Ut (_type_): _description_
            V (_type_): _description_

        Returns:
            _type_: _description_
        """        """Confirm that determinant of R is 1,
            or negate the last term of V to fix it
            Note: this algorithm works for noiseless case
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
        a_bar = self.mean_point(self.points)
        b_bar = self.mean_point(b.points)

        return b_bar - np.dot(R, a_bar)
    
    
    def is_almost_one(self, det):
        """_summary_

        Args:
            det (_type_): _description_

        Returns:
            _type_: _description_
        """        
        return abs(det - 1) <= 1e-9
    
    def mean_point(self, points):
        """_summary_

        Args:
            points (_type_): _description_
        """        
        mean = [0, 0, 0]

        for point in points:
            for i in range(3):
                mean[i] += point[i]
        
        for i in range(3):
            mean[i] = mean[i] / len(points)

        return mean