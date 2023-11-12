import numpy as np
from pointSet import PointSet
from pivotCalibration import pivot_calibration
from pytransform3d.transformations import transform_from, transform


class FindingTipCT:

    def __init__(self, emPivot, ctFid, emFid, emNav, emOutput, dist):
        """_summary_

        Args:
            emPivot (EMPivot): An object storing information from the 
            EMPivot class
            ctFid (CTFiducials): An object storing information from the 
            CTFiducials class
            emFid (EMFiducials): An object storing information from the 
            EMFiducials class
            emNav (EMNav): An object storing information from the 
            EMNav class
            emOutput (EMOutput): An object to output data to pa2 .txt output files
            dist (DistortionCorrection): An object used to undistort arrays of data
        """       
        #create instances of objects from data files
        self.emPivot = emPivot
        self.ctFid = ctFid
        self.emFid = emFid
        self.emNav = emNav
        self.emOutput = emOutput
        self.dist = dist
       
        

    def recalibrate(self):
        """Find a new EMPivot location based on the undistorted EMPivot array

        Returns:
            1x3 array: EM Pivot location in EM coordinates
        """     
        #Undistort the array using the distortion correction class   
        correctedGArray = self.dist.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)
        #pivot calibration with the undistorited array
        return pivot_calibration(correctedGArray, self.emPivot.numFrames, self.emPivot.numProbeMarkers)
            
    
    def find_fid_pointer_locs(self):
        """Find the location of fiducials in EM coordinates

        Returns:
            array: Array of 3D coordinates of EM fiducials
        """        
        #for dimension purposes in calculations p_dimple needs to have 4 values 
        p_dimple4D = np.append(self.p_dimple, 1)
        #undistort relevant arrays
        correctedEMFid = self.dist.undistort_array(self.emFid.GArray, self.emFid.numFrames)
        correctedEMPiv = self.dist.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)

        Gj_set = PointSet(correctedEMPiv[0])

        fidMatrix = np.empty((1, 3))
        #matrix of fiducial locations
        for k in range(self.emFid.numFrames):
            #Find the registration from EM pivot coordiantes to fiducial locations
            #And transform EM pivot with this registration
            fid_set = PointSet(correctedEMFid[k])
            R, p = Gj_set.find_registration(fid_set)
            Freg = transform_from(R, p)
            fid = transform(Freg, p_dimple4D)
            fidMatrix = np.vstack((fidMatrix, fid[:3]))
        
        return fidMatrix

    def find_em_ct_f_reg(self):
        """
            Find the Freg between EM and CT coordinates and save it as a 
            class attribute
        """
        #Get the new pivot coordinates after undistorting CiExpected
        self.p_dimple = self.recalibrate()

        #Get the array of ct Fiducials
        b_i = self.ctFid.bArray
        b_i_set = PointSet(b_i)

        fidSet = PointSet(self.find_fid_pointer_locs())
        #call function written in programming 1
        R, p = fidSet.find_registration(b_i_set)
        #this is from pyratransform
        self.F_reg = transform_from(R, p)
    
    def find_emNav_in_ct(self):
        """
        Find the pivot location in CT.
        """
        #undistort relevant arrays
        correctedEMNav = self.dist.undistort_array(self.emNav.GArray, self.emNav.numFrames)
        correctedEMPiv = self.dist.undistort_array(self.emPivot.GArray, self.emPivot.numFrames)
        
        Gj_set= PointSet(correctedEMPiv[0])
        p_dimple4D = np.append(self.p_dimple, 1)

        for k in range(self.emNav.numFrames):
            #Find the registration from EM pivot coordiantes to nav locations
            #And transform EM pivot with this registration
            nav_set = PointSet(correctedEMNav[k])
            R, p = Gj_set.find_registration(nav_set)
            Freg = transform_from(R, p)
            nav = transform(Freg, p_dimple4D)
            #Then transform the location to CT coordinates and output it
            self.emOutput.add_pivot(transform(self.F_reg, nav)[:3])
        
        
   




            
            
            

