from pointSet import PointSet
from pytransform3d.transformations import transform_from, transform
import pivotCalibration as pivotCalibration

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
   
    djSet = PointSet(dj)

    #Find transformation FD and apply it to Hs to get to Pj
    Pj = []
    for k in range(optPivot.numFrames):
        DjSet = PointSet(Dj[k])

        R_D, p_D = DjSet.find_registration(djSet)

        F_D = transform_from(R_D, p_D)

        Hj = optPivot.HArray[k]

        Hj_4d = [point + [1] for point in Hj]

        Pj_k = transform(F_D, Hj_4d)

        Pj.append([point[:-1] for point in Pj_k])
    
    return pivotCalibration.pivot_calibration(Pj, optPivot.numFrames, optPivot.numOptProbeMarkers)