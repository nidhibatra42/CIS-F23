import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from

def opt_pivot_calibration(Gj):
    
    #Find Go
    Go = np.mean(Gj)
    #find gj
    gj = Gj - Go
    #Find transformation Fk 
   # Fk = np.dot(Gj, np.linalg.inv(gj))

    GjSet = PointSet(Gj)
    gjSet = PointSet(gj)

    R_fK, p_fK = GjSet.find_registration(gjSet)

    F_GK = transform_from(R_fK, p_fK)

    t_G = np.dot(np.linalg.inv(F_GK, Gj))

    return np.dot(F_GK, t_G) #p_dimple 



