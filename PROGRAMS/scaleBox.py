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

class BoxScale:
    
    degree = 5

    def __init__(self, fileName, inputFolder, outputFolder):
        self.fileName = fileName
        self.outputFolder = outputFolder
        self.calRead = CalReadings(inputFolder, fileName)
        self.calObj = CalBody(inputFolder, fileName)
        self.emPivot = EMPivot(inputFolder, fileName)
        self.ctFid = CTFiducials(inputFolder, fileName)
        self.emFid = EMFiducials(inputFolder, fileName)
        self.emNav = EMNav(inputFolder, fileName)
        self.emOutput = EMOutputWriter(outputFolder, fileName, self.emNav.numFrames)
        #find actual from expected using function from assignment 1, 4 
        
        self.p1Output = OutputWriter(outputFolder, fileName, self.calObj.numEMCalMarkers, self.calRead.numFrames )
        self.ci = self.calRead.cArray


    #it does what it says on the tin
    def get_ci_expecteds(self):
        self.ciExpected = []
        for i in range(self.calRead.numFrames):
            self.p1Output.add_frame(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))
        o1Filename = self.outputFolder + '/' + self.fileName + '-output1.txt'
        #self.calObj.numEMCalMarkers, self.calRead.numFrames
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
        

    #need to determine bounding box to scale values
    def create_scale_box(self):
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
    
    def scale_to_box(self, point, frame):
        scaledPoint = []
        for i in range(3):
            scaledPoint.append((point[i] - self.mins[frame][i]) / self.maxes[frame][i] - self.mins[frame][i])
        
        return scaledPoint
            
    
    def single_coor_bernstein(self, coor, i):
        return comb(self.degree, i) * pow(coor, i) * pow((1 - coor), (self.degree - i))


    #Distortion correction for points -> list of the points in a given frame
    def create_F(self, points, k):
        F = []

        scaledPoints = []
        for point in points:
            scaledPoints.append(self.scale_to_box(point, k))

        for point in scaledPoints:
            F.append(self.create_f_row(point))
        
        return F

    def create_f_row(self, point):
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


    def generate_distortion_correction(self):
        self.calMatrices = []
        for k in range(self.calRead.numFrames):
            F = self.create_F(self.ci[k], k)

            calMatrix = np.linalg.lstsq(F, self.ciExpected[k], None)
            self.calMatrices.append(calMatrix[0])
        
    
    def recalibrate(self):
        #New p dimple
        self.generate_distortion_correction()

        correctedGArray = self.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)

        return pivot_calibration(correctedGArray, self.emPivot.numFrames, self.emPivot.numProbeMarkers)
            

    def bj_emcoords(self):
        #Return bj in em coordinates
        p_dimple = self.recalibrate()

        correctedEMFid = self.undistort_array(self.emFid.GArray, self.emFid.numFrames)

        emFidMeans = []
        for frame in correctedEMFid:
            emFidMeans.append(mean_point(frame))

        finalEMFid = []
        for point in emFidMeans:
            finalEMFid.append(np.add(point, p_dimple))
        
        return finalEMFid
        
    def registration_frame(self):
        #ct coordinates
        b_i = self.ctFid.bArray
        b_i_set = PointSet(b_i)

        #em coordinates
        b_j = self.problem_4()
        b_j_set = PointSet(b_j)

        R_D, p_D = b_j_set.find_registration(b_i_set)
        FD = transform_from(R_D, p_D)

        return FD
    #tip location in ct coordinates
    def tip_ct(self):
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
            self.emOutput.add_pivot(transform(self.problem_5(), point4D ))


    def undistort_array(self, points, numFrames):
        correctedArray = []
        for k in range(numFrames):
            correctedArray.append([])
            for point in points[k]:
                newPoint = np.dot(np.transpose(self.create_f_row(self.scale_to_box(point, k))), self.calMatrices[k])
                correctedArray[k].append(newPoint)
        
        return correctedArray
    
