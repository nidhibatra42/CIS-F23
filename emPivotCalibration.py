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
   # t_g = []
    for k in range(emPivot.numFrames):
        GjSet = PointSet(Gj[k])
        gjSet = PointSet(gj[k])

        R_fK, p_fK = GjSet.find_registration(gjSet)
        F_G_k = (transform_from(R_fK, p_fK))

        F_G.append(F_G_k)
        #t_g.append(np.dot(np.linalg.inv(F_G_k), Gj[k]))
        
    t_g = np.mean(Gj, axis=0)
  #  p_dimple = np.linalg.lstsq(F_G, t_g)
    p_dimple = least_squares_minimizer(emPivot.numFrames, F_G, t_g, Gj)
    
    return p_dimple

def least_squares_minimizer(numFrames, F_G, t_g, Gj):
        # Minimize the least squares error.
    for i in range(100):
        error = 0
        for k in range(numFrames):
            error += np.sum((F_G[k] * t_g - Gj[k])**2)

        # Update the estimated pivot location.
        t_g = t_g - np.dot(F_G[0].T, (F_G[0] * t_g - Gj[0])) / np.dot(F_G[0].T, F_G[0])
    
    return t_g