import numpy as np
import pandas as pd


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

        Gj_set = PointSet(correctedEMPiv[0])

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
        
        Gj_set= PointSet(correctedEMPiv[0])
        p_dimple4D = np.append(self.p_dimple, 1)

        for k in range(self.emNav.numFrames):
            nav_set = PointSet(correctedEMNav[k])
            R, p = Gj_set.find_registration(nav_set)
            Freg = transform_from(R, p)
            nav = transform(Freg, p_dimple4D)
            self.emOutput.add_pivot(transform(self.F_reg, nav)[:3])
        
        




            
            
            

