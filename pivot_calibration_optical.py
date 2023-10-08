import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from

def pivot_calibration_optical(Dj, Hj):
    #Find Go
    Do = np.mean(Dj)
    #find gj
    dj = Dj - Do
    #Find transformation FD 
 
    DjSet = PointSet(Dj)
    djSet = PointSet(dj)

    R_D, p_D = DjSet.find_registration(djSet)

    F_D = transform_from(R_D, p_D)

    Pj = np.dot(F_D, Hj)
    return em_pivot_calibration(Pj)




