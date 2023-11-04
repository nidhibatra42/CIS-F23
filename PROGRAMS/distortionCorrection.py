import pandas as pd
import numpy as np
from math import comb
from expectedValues import expected_values

class DistortionCorrection:

    def __init__(self, calRead, calObj, p1Output):
        self.degree = 5
        self.calRead = calRead
        self.calObj = calObj
        self.p1Output = p1Output
        self.ci = self.calRead.cArray

     ## Function to create a bounding box for scaling values

    def create_scale_box(self):
        """
        Create a bounding box to scale values in ci.
        """
        #Max and min store the maxes and mins of each data frame as [x_max_i, y_max_i, z_max_i]
        self.maxes = []
        self.mins = []
        tolerance = 1.01
        for k in range(len(self.ci)):
            ci_df = pd.DataFrame(self.ci[k], columns=['x', 'y', 'z'])
            max = []
            max.append(ci_df.x.max() * tolerance)
            max.append(ci_df.y.max() * tolerance)
            max.append(ci_df.z.max() * tolerance)
            min = []
            min.append(ci_df.x.min() * tolerance)
            min.append(ci_df.y.min() * tolerance)
            min.append(ci_df.z.min() * tolerance)
            self.maxes.append(max)
            self.mins.append(min)

    
    # Function to scale a point to the bounding box
    def scale_to_box(self, point, frame):
        """
        Scale a point to fit within the bounding box.
        """
        scaledPoint = []
        for i in range(3):
            scaledPoint.append((point[i] - self.mins[frame][i]) / self.maxes[frame][i] - self.mins[frame][i])
        
        return scaledPoint
    
    # Function to compute a single coordinate of Bernstein polynomial
    def single_coor_bernstein(self, coor, i):
        """
        Calculate a single coordinate of the Bernstein polynomial for distortion correction.
        """
        return comb(self.degree, i) * pow(coor, i) * pow((1 - coor), (self.degree - i))

    #Function to get expected values for ci
    def get_ci_expecteds(self):
        """
        Calculate and store expected values for ci.
        """
        self.ciExpected = []
        for i in range(self.calRead.numFrames):
             # Add frame with expected values
            self.p1Output.add_frame(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))
            self.ciExpected.append(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))
        

        # Function to create matrix F for distortion correction
    def create_F(self, points, k):
        """
        Create a matrix F for distortion correction based on scaled points and frame.
        """
        F = []

        scaledPoints = []
        for point in points:
            scaledPoints.append(self.scale_to_box(point, k))

        for point in scaledPoints:
            F.append(self.create_f_row(point))
        
        return F

    # Function to create a row in matrix F
    def create_f_row(self, point):
        """
        Create a row in the matrix F using a scaled point.
        """
        f_row = []
        for i in range(self.degree + 1):
            for j in range(self.degree + 1):
                for k in range(self.degree + 1):
                    bs = []
                    bs.append(self.single_coor_bernstein(point[0], i))
                    bs.append(self.single_coor_bernstein(point[1], j))
                    bs.append(self.single_coor_bernstein(point[2], k))

                    f_row.append(bs[0] * bs[1] * bs[2])
        return f_row


    # Function to generate distortion correction
    def generate_distortion_correction(self):
        """
        Generate distortion correction matrices for each frame.
        """
        self.calMatrices = []
        for k in range(self.calRead.numFrames):
            F = self.create_F(self.ci[k], k)
            calMatrix = np.linalg.lstsq(F, self.ciExpected[k], None)
            self.calMatrices.append(calMatrix[0])

        # Function to undistort an array of points
    def undistort_array(self, points, numFrames):
        """
        Undistort an array of points based on distortion correction matrices.
        """
        correctedArray = []
        for k in range(numFrames):
            correctedArray.append([])
            for point in points[k]:
                newPoint = np.dot(np.transpose(self.create_f_row(self.scale_to_box(point, k))), self.calMatrices[k])
                correctedArray[k].append(newPoint)
        
        return correctedArray

