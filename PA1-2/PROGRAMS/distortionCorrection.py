import pandas as pd
import numpy as np
from math import comb
from expectedValues import expected_values

class DistortionCorrection:
    """
        A class that stores all relevant functions to perform a 
        distortion correction on an array of points
    """
    def __init__(self, calRead, calObj):
        """
        Args:
            calRead (calReadings): An object that stores information from
              the calReadings class
            calObj (calBody): An object that stores information from 4
            the calBody class
        """
        #Bernstein polynomial degree        
        self.degree = 5
        self.calRead = calRead
        self.calObj = calObj
        self.ci = self.calRead.cArray

     

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
            #Add the maximum of each coordinate in the frame
            max.append(ci_df.x.max() * tolerance)
            max.append(ci_df.y.max() * tolerance)
            max.append(ci_df.z.max() * tolerance)
            min = []
            #Add the minimum of each coordinate in the frame
            min.append(ci_df.x.min() * tolerance)
            min.append(ci_df.y.min() * tolerance)
            min.append(ci_df.z.min() * tolerance)
            #storing maxes and mins
            self.maxes.append(max)
            self.mins.append(min)

    
    
    def scale_to_box(self, point, frame):
        """Scale a point to fit within the bounding box for use
          in distortion correction

        Args:
            point (1x3 array): 3d coordinate to be scaled
            frame (int): The frame which the point comes from

        Returns:
            1x3 array : Scaled point from 0 to 1 for all coordinates
        """ 
        scaledPoint = []
        for i in range(3):
            #formula for scaling a point
            scaledPoint.append((point[i] - self.mins[frame][i]) / self.maxes[frame][i] - self.mins[frame][i])
        
        return scaledPoint
    
    
    def single_coor_bernstein(self, coor, i):
        """Calculate a single coordinate of the Bernstein polynomial for distortion correction.

        Args:
            coor (int): Single scaled coordinate (x, y, or z)
            i (int): Secondary degree to scale 

        Returns:
            float: The result of the Bernstein polynomial on the point (i.e. B(x))
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
            self.ciExpected.append(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))
        

       
    def create_F(self, points, k):
        """Create Bernstein polynomial matrix

        Args:
            points (list of 1x3 arrays): List of points
            k (int): frame number of the points

        Returns:
            matrix: Return an F matrix containing all of the Bernstein
            calculations for each point in the frame. Size len(points)
            x 125
        """
        F = []

        #Get all of the scaled points to use with Bernstein
        scaledPoints = []
        for point in points:
            scaledPoints.append(self.scale_to_box(point, k))

        #For each point, create a row of 125 Bernstein values and add it
        #to the matrix
        for point in scaledPoints:
            F.append(self.create_f_row(point))
        
        return F

   
    def create_f_row(self, point):
        """Create a row for the tensor form interpolation polynomial
            for the given point

        Args:
            point (1x3 array): Scaled 3D point (all coordinates 0 - 1)

        Returns:
            1 x 125 array: Sinhle row of the tensor form interpolation
        """        
        f_row = []
         
        #For every permutation 0 -> the Bernstein degree
        for i in range(self.degree + 1):
            for j in range(self.degree + 1):
                for k in range(self.degree + 1):
                    bs = []
                    #Add the Bernstein polynomial of each coordinate to the row
                    bs.append(self.single_coor_bernstein(point[0], i))
                    bs.append(self.single_coor_bernstein(point[1], j))
                    bs.append(self.single_coor_bernstein(point[2], k))
                    #add the correct product of the bernsteins to the row 
                    f_row.append(bs[0] * bs[1] * bs[2])
        return f_row



    def generate_distortion_correction(self):
        """
        Generate distortion correction matrices for each frame.
        """
        self.calMatrices = []
        for k in range(self.calRead.numFrames):
            F = self.create_F(self.ci[k], k)
            #using least squares as outlined in procedure 
            calMatrix = np.linalg.lstsq(F, self.ciExpected[k], None)
            self.calMatrices.append(calMatrix[0])


    def undistort_array(self, points, numFrames):
        """Undistort an array of points using the calculated class 
            calibration matrix

        Args:
            points (list of 1x3 arrays): List of 3D points
            numFrames (int): Number of frames in the list

        Returns:
            len(points) x 3 array: List of undistorted 3D points
        """        
        correctedArray = []
        for k in range(numFrames):
            correctedArray.append([])
            for point in points[k]:
                #undistort using calibration matrix we found
                newPoint = np.dot(np.transpose(self.create_f_row(self.scale_to_box(point, k))), self.calMatrices[k])
                correctedArray[k].append(newPoint)
        
        return correctedArray
