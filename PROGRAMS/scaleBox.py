import numpy as np
import pandas as pd
from math import comb
from expectedValues import expected_values
from calReadings import CalReadings
from emPivot import EMPivot
from pivotCalibration import pivot_calibration


class BoxScale:
    
    degree = 5

    def __init__(self, fileName, inputFolder):
        self.calRead = CalReadings(inputFolder, fileName)
        self.emPivot = EMPivot(inputFolder, fileName)
  
        #find actual from expected using function from assignment 1, 4 
        self.ciExpected = []
        for i in range(self.calRead.numFrames):
            self.ciExpected.add_frame(expected_values(self.calRead.dArray[i], self.calRead.aArray[i], self.calObj.dArray, self.calObj.aArray, self.calObj.cArray))

        self.ci = self.emPivot.GArray



    #need to determine bounding box to scale values
    def create_scale_box(self):
        #Max and min store the maxes and mins of each data frame as [x_max_i, y_max_i, z_max_i]
        self.maxes = []
        self.mins = []
        tolerance = 1.01
        for k in range(len(self.ci)):
            ci_df = pd.DataFrame(self.ci[k], columns=['x', 'y', 'z'])
            max = []
            max.append(ci_df.x.max * tolerance)
            max.append(ci_df.y.max * tolerance)
            max.append(ci_df.z.max * tolerance)
            min = []
            min.append(ci_df.x.max * tolerance)
            min.append(ci_df.y.max * tolerance)
            min.append(ci_df.z.max * tolerance)
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

    def create_f_row(self, point):
        f_row = []
        for i in range(self.maxDegree + 1):
            for j in range(self.maxDegree + 1):
                for k in range(self.maxDegree + 1):
                    bs = []
                    bs.append(self.single_coor_bernstein(point[0], i))
                    bs.append(self.single_coor_bernstein(point[1], j))
                    bs.append(self.single_coor_bernstein(point[2], k))

                    f_row.append(bs[0] * bs[1] * bs[2])


    def distortion_correction(self):
        correctedPoints = []
        for k in range(self.calRead.numFrames):
            F = self.create_F(self.ci[k], k)

            calMatrix = np.linalg.lstsq(F, self.ciExpected[k], None)
            correctedPoints.append(np.dot(F, calMatrix))
        
        return correctedPoints
    
    def recalibrate(self):
        newPoints = self.distortion_correction()
        return pivot_calibration(newPoints, self.emPivot.numFrames, self.emPivot.numProbeMarkers)
            


