import numpy as np
from pointSet import PointSet
from emPivotCalibration import em_pivot_calibration
from pytransform3d.transformations import transform_from

def opt_pivot_calibration(Dj, Hj):
    """_summary_

    Args:
        Dj (_type_): _description_
        Hj (_type_): _description_

    Returns:
        _type_: _description_
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




