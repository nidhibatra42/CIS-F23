import numpy as np
from PROGRAMS.pointSet import PointSet
from PROGRAMS.emPivotCalibration import em_pivot_calibration
from pytransform3d.transformations import transform_from, transform
import PROGRAMS.meanPoint as meanPoint
import PROGRAMS.pivotCalibration as pivotCalibration

def opt_pivot_calibration(optPivot, calBody):
    """_summary_

    Args:
        Dj (numpy.ndarray): Array of 3D coordinates of base markers on the calibration object.
        Hj (numpy.ndarray): Array of 3D coordinates of the optical probe markers.

    Returns:
        numpy.ndarray: Position of the dimple relative to the Optical tracker base coordinate system.
    """  
    #Find D0
    Dj = optPivot.DArray
    #find dj
    dj = calBody.dArray
    #Find transformation FD 
 
    djSet = PointSet(dj)

    Pj = []
    for k in range(optPivot.numFrames):
        DjSet = PointSet(Dj[k])

        R_D, p_D = DjSet.find_registration(djSet)

        F_D = transform_from(R_D, p_D)

        Hj = optPivot.HArray[k]

        Hj_4d = [point + [1] for point in Hj]

        Pj_k = transform(F_D, Hj_4d)

        Pj.append([point[:-1] for point in Pj_k])
    
    Po = meanPoint.mean_point(Pj[0])

    #find gj
    pj = []
    #for each frame

    for j in range(optPivot.numOptProbeMarkers):
        pj.append([])
        #for each coordinate in the point
        for i in range(3):
            pj[j].append(Pj[0][j][i] - Po[i])

    pjSet = PointSet(pj)

    #Create arrays for F_G[k] and t_g[k]
    R_fks = []
    p_fks = []
    

    for k in range(optPivot.numFrames):
        PjSet = PointSet(Pj[k])

        R_fK, p_fK = pjSet.find_registration(PjSet)

        R_fks.append(R_fK)
        p_fks.append(p_fK)

    
    return pivotCalibration.pivot_calibration(R_fks, p_fks)
    


        
"""  
   Hj = optPivot.HArray

    Ho = meanPoint.mean_point(Hj[0])

    hj = []

    for j in range(optPivot.numOptProbeMarkers):
        hj.append([])
        #for each coordinate in the point
        for i in range(3):
            hj[j].append(Hj[0][j][i] - Ho[i])


    Pj = np.dot(F_D_inv, Hj)
    pj = np.dot(F_D_inv, hj)

    pjSet = PointSet(pj)
    #Create arrays for F_G[k] and t_g[k]
    R_fks = []
    p_fks = []
    

    for k in range(optPivot.numFrames):
        PjSet = PointSet(Pj[k])

        R_fK, p_fK = pjSet.find_registration(PjSet)

        R_fks.append(R_fK)
        p_fks.append(p_fK)

    
    return pivotCalibration.pivot_calibration(R_fks, p_fks)

"""


