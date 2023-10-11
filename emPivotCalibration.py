import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
from emPivot import EMPivot

def em_pivot_calibration(emPivot):
    """_summary_

    Args:
        emPivot (EMPivot): _description_
    """     
    Gj = emPivot.GArray
    #Find Go
    Go = np.mean(Gj)
    #find gj
    gj = Gj - Go
    #Find transformation Fk 

    #Create arrays for F_G[k] and t_g[k]
    F_G = []
    t_g = []
    for k in range(emPivot.numFrames):
        GjSet = PointSet(Gj[k])
        gjSet = PointSet(gj[k])

        R_fK, p_fK = GjSet.find_registration(gjSet)
        F_G_k = (transform_from(R_fK, p_fK))

        F_G.append(F_G_k)
        t_g.append(np.dot(np.linalg.inv(F_G_k), Gj[k]))
        
    p_dimple = np.linalg.lstsq(F_G, t_g)

    
    return p_dimple


