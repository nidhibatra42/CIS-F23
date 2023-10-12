import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
from pytransform3d.rotations import quaternion_from_matrix
from emPivot import EMPivot
import meanPoint
import pivotCalibration

def em_pivot_calibration(emPivot):
    """_summary_

    Args:
        emPivot (EMPivot): _description_
    """     
    Gj = emPivot.GArray

    #Find Go as the mean of the first frame
    Go = meanPoint.mean_point(Gj[0])

    #find gj
    gj = []
    #for each frame

    for j in range(emPivot.numProbeMarkers):
        gj.append([])
        #for each coordinate in the point
        for i in range(3):
            gj[j].append(Gj[0][j][i] - Go[i])

    gjSet = PointSet(gj)

    #Create arrays for F_G[k] and t_g[k]
    R_fks = []
    p_fks = []
    

    for k in range(emPivot.numFrames):
        GjSet = PointSet(Gj[k])

        R_fK, p_fK = gjSet.find_registration(GjSet)

        R_fks.append(R_fK)
        p_fks.append(p_fK)

    
    return pivotCalibration.pivot_calibration(R_fks, p_fks)

    

        
    
    



        
    
