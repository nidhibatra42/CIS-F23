import numpy as np
import pandas as pd
from math import comb
from expectedValues import expected_values
from calReadings import CalReadings
from emPivot import EMPivot
from ctFiducials import CTFiducials
from emFiducials import EMFiducials
from pointSet import PointSet
from emNav import EMNav
from pivotCalibration import pivot_calibration
from pytransform3d.transformations import transform_from, transform
from meanPoint import mean_point
from emOutput import EMOutputWriter
from outputWriter import OutputWriter
from calBody import CalBody
from point import Point

class FindingTipCT:
    
    #storing bernstein degree so its easier to manipulate
    degree = 5

    def __init__(self, fileName, inputFolder, outputFolder):
       
        self.fileName = fileName
        self.outputFolder = outputFolder
        #create instances of objects from data files
        self.calRead = CalReadings(inputFolder, fileName)
        self.calObj = CalBody(inputFolder, fileName)
        self.emPivot = EMPivot(inputFolder, fileName)
        self.ctFid = CTFiducials(inputFolder, fileName)
        self.emFid = EMFiducials(inputFolder, fileName)
        self.emNav = EMNav(inputFolder, fileName)
        self.emOutput = EMOutputWriter(outputFolder, fileName, self.emNav.numFrames)
        self.p1Output = OutputWriter(outputFolder, fileName, self.calObj.numEMCalMarkers, self.calRead.numFrames )
        self.ci = self.calRead.cArray


    #Function to get expected values for ci
    def get_ci_expecteds(self):
        """
        Calculate and store expected values for ci.
        """
        self.ciExpected = []
        for i in range(self.calRead.numFrames):
             # Add frame with expected values
            self.p1Output.add_frame(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))
        o1Filename = self.outputFolder + '/' + self.fileName + '-output1.txt'
        o1Data = pd.read_csv(o1Filename, delimiter=',', skiprows=[0], names=['x', 'y', 'z'])
        x_coors = o1Data['x']
        y_coors = o1Data['y']
        z_coors = o1Data['z']

        self.ciExpected = []
        for k in range (self.calRead.numFrames):
            self.ciExpected.append([])
            for j in range(self.calObj.numEMCalMarkers):
                p = Point(x_coors[k * self.calObj.numEMCalMarkers + j], y_coors[k * self.calObj.numEMCalMarkers + j], z_coors[k * self.calObj.numEMCalMarkers + j]) 
                self.ciExpected[k].append(p.to_array())  
        

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
            min.append(ci_df.x.max() * tolerance)
            min.append(ci_df.y.max() * tolerance)
            min.append(ci_df.z.max() * tolerance)
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
        
    # Function to recalibrate pivot
    def recalibrate(self):
        """
        Recalibrate and return the recalibrated pivot.
        """
        #New p dimple
        self.generate_distortion_correction()

        correctedGArray = self.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)

        return pivot_calibration(correctedGArray, self.emPivot.numFrames, self.emPivot.numProbeMarkers)
            
    # Function to calculate bj in EM coordinates
    def bj_emcoords(self):
        """
        Calculate and return bj in EM coordinates by applying recalibration.
        """
        p_dimple = self.recalibrate()

        correctedEMFid = self.undistort_array(self.emFid.GArray, self.emFid.numFrames)

        emFidMeans = []
        for frame in correctedEMFid:
            emFidMeans.append(mean_point(frame))

        finalEMFid = []
        for point in emFidMeans:
            finalEMFid.append(np.add(point, p_dimple))
        
        return finalEMFid
        
    # Function to compute the registration frame
    def registration_frame(self):
        """
        Calculate and return the registration frame for mapping between CT and EM coordinates.
        """
        #ct coordinates
        b_i = self.ctFid.bArray
        b_i_set = PointSet(b_i)

        #em coordinates
        b_j = self.bj_emcoords()
        b_j_set = PointSet(b_j)

        R_D, p_D = b_j_set.find_registration(b_i_set)
        FD = transform_from(R_D, p_D)

        return FD
   
    #Function to get the tip location in CT coordinates
    def tip_ct(self):
        """
        Calculate and record the tip location in CT coordinates.
        """
        #Return bj in em coordinates
        p_dimple = self.recalibrate()

        correctedEMNav = self.undistort_array(self.emNav.GArray, self.emNav.numFrames)

        emNavMeans = []
        for frame in correctedEMNav:
            emNavMeans.append(mean_point(frame))

        finalEMNav = []
        for point in emNavMeans:
            finalEMNav.append(np.add(point, p_dimple))
        
        for point in finalEMNav:
            point4D = np.append(point, 1)
            self.emOutput.add_pivot(transform(self.registration_frame(), point4D ))


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
    
