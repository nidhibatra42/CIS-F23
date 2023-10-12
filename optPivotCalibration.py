import numpy as np
from pointSet import PointSet
from emPivotCalibration import em_pivot_calibration
import meanPoint
import pivotCalibration

def opt_pivot_calibration(optPivot, calBody):
    """_summary_

    Args:
        Dj (_type_): _description_
        Hj (_type_): _description_

    Returns:
        _type_: _description_
    """    
    #Find D0
    Dj = optPivot.DArray
    #find dj
    dj = calBody.dArray
    #Find transformation FD 
 
    DjSet = PointSet(Dj)
    djSet = PointSet(dj)

    R_D, p_D = DjSet.find_registration(djSet)

    F_D = transform_from(R_D, p_D)

    Pj = np.dot(F_D, Hj)
    return em_pivot_calibration(Pj)




