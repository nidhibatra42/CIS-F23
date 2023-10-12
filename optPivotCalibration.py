import numpy as np
from pointSet import PointSet
from emPivotCalibration import em_pivot_calibration
from pytransform3d.transformations import transform_from

def opt_pivot_calibration(Dj, Hj):
    """Perform optical pivot calibration and determine the position of the dimple.

    Args:
        Dj (numpy.ndarray): Array of 3D coordinates of base markers on the calibration object.
        Hj (numpy.ndarray): Array of 3D coordinates of the optical probe markers.

    Returns:
        numpy.ndarray: Position of the dimple relative to the Optical tracker base coordinate system.
    """  
    #Find D0
    Do = np.mean(Dj)
    #find dj
    dj = Dj - Do
    #Find transformation FD 
 
    DjSet = PointSet(Dj)
    djSet = PointSet(dj)

    R_D, p_D = DjSet.find_registration(djSet)

    F_D = transform_from(R_D, p_D)

    Pj = np.dot(F_D, Hj)
    return em_pivot_calibration(Pj)




