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
from pivotCalibration import pivot_calibration, get_pointer_locations
from pytransform3d.transformations import transform_from, transform
from meanPoint import mean_point
from emOutput import EMOutputWriter
from outputWriter import OutputWriter
from calBody import CalBody
from point import Point


class BoxScale:
    
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

        correctedCExpecteds = self.undistort_array(self.ciExpected, self.calRead.numFrames)
        
        return pivot_calibration(correctedGArray, self.emPivot.numFrames, self.emPivot.numProbeMarkers)
            
    # Function to calculate bj in EM coordinates
    def bj_emcoords(self):
        """
        Calculate and return bj in EM coordinates by applying recalibration.
        """
        self.p_dimple = self.recalibrate()

        correctedEMFid = self.undistort_array(self.emFid.GArray, self.emFid.numFrames)

        emFidMeans = []
        for frame in correctedEMFid:
            emFidMeans.append(mean_point(frame))

        finalEMFid = []
        for point in emFidMeans:
            finalEMFid.append(np.add(point, self.p_dimple))
        
        return finalEMFid
        
    # Function to compute the registration frame
    def registration_frame(self):
        """
        Calculate and return the registration frame for mapping between CT and EM coordinates.
        """
        correctedEMFid = self.undistort_array(self.emFid.GArray, self.emFid.numFrames)
        
        fidMatrix = get_pointer_locations(correctedEMFid, self.emFid.numFrames, self.emFid.numProbeMarkers, self.p_dimple)

        #ct coordinates
        b_i = self.ctFid.bArray
        b_i_set = PointSet(b_i)

        #em coordinates
        b_j_set = PointSet(fidMatrix)

        R_D, p_D = b_j_set.find_registration(b_i_set)
        FD = transform_from(R_D, p_D)

        return FD
   
    #Function to get the tip location in CT coordinates
    def tip_ct(self):
        """
        Calculate and record the tip location in CT coordinates.
        """
        self.p_dimple = self.recalibrate()
        correctedEMNav = self.undistort_array(self.emNav.GArray, self.emNav.numFrames)

        emNavPoints = get_pointer_locations(correctedEMNav, self.emNav.numFrames, self.emNav.numProbeMarkers, self.p_dimple)
        
        F_reg = self.p5_2()
        for point in emNavPoints:
            self.emOutput.add_pivot(transform(F_reg, point)[:3])


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
    
    def p4_2(self):
        p_dimple4D = np.append(self.p_dimple, 1)
        correctedEMFid = self.undistort_array(self.emFid.GArray, self.emFid.numFrames)
        correctedEMPiv = self.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)

        G_0 = mean_point(correctedEMPiv[0])

        Gj = []

        #for each point
        for j in range(self.emPivot.numProbeMarkers):
            Gj.append([])
            #for each coordinate in the point
            for i in range(3):
                Gj[j].append(correctedEMPiv[0][j][i] - G_0[i])

        Gj_set= PointSet(Gj)

        fidMatrix = np.empty((1, 3))

        for k in range(self.emFid.numFrames):
            fid_set = PointSet(correctedEMFid[k])
            R, p = Gj_set.find_registration(fid_set)
            Freg = transform_from(R, p)
            fid = transform(Freg, p_dimple4D)
            fidMatrix = np.vstack((fidMatrix, fid[:3]))
        
        return fidMatrix

    def p5_2(self):
        self.p_dimple = self.recalibrate()

        b_i = self.ctFid.bArray
        b_i_set = PointSet(b_i)

        fidSet = PointSet(self.p4_2())

        R, p = fidSet.find_registration(b_i_set)
        self.F_reg = transform_from(R, p)
    
    def p6_2(self):
        correctedEMNav = self.undistort_array(self.emNav.GArray, self.emNav.numFrames)
        correctedEMPiv = self.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)

        G_0 = mean_point(correctedEMPiv[0])

        Gj = []

        #for each point
        for j in range(self.emPivot.numProbeMarkers):
            Gj.append([])
            #for each coordinate in the point
            for i in range(3):
                Gj[j].append(correctedEMPiv[0][j][i] - G_0[i])

        Gj_set= PointSet(Gj)
        p_dimple4D = np.append(self.p_dimple, 1)

        for k in range(self.emNav.numFrames):
            nav_set = PointSet(correctedEMNav[k])
            R, p = Gj_set.find_registration(nav_set)
            Freg = transform_from(R, p)
            nav = transform(Freg, p_dimple4D)
            self.emOutput.add_pivot(transform(self.F_reg, nav)[:3])
        
        




            
            
            

