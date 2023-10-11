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
       # Calculate t_g[k] by applying the inverse transformation to each point in Gj[k]
        t_g_k = np.zeros((emPivot.numProbeMarkers, 3))
        for i in range(emPivot.numProbeMarkers):
            t_g_k[i] = np.dot(np.linalg.inv(F_G_k[:3, :3]), Gj[k][i] - F_G_k[:3, 3])

        t_g.append(t_g_k)

    # Use np.linalg.lstsq to estimate p_dimple
    t_g = np.array(t_g).reshape(-1, 3)  # Reshape t_g for the least squares optimization

    A = np.zeros((emPivot.numFrames * emPivot.numProbeMarkers, 16))
    for i in range(emPivot.numFrames):
        for j in range(emPivot.numProbeMarkers):
            A[i * emPivot.numProbeMarkers + j] = F_G[i].flatten()

    p_dimple, _, _, _ = np.linalg.lstsq(A, t_g, rcond=None)

    return p_dimple

