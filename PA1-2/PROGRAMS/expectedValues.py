import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from

def expected_values(Dj, Aj, dj, aj, cj):
    """Calculate the expected positions of markers on the calibration object.

    Args:
        Dj (list of lists): List of 3D coordinates of electromagnetic base markers.
        Aj (list of lists): List of 3D coordinates of optical calibration markers on the calibration object.
        dj (list of lists): List of 3D coordinates of electromagnetic probe markers.
        aj (list of lists): List of 3D coordinates of optical probe markers.
        cj (list of lists): List of 3D coordinates of electromagnetic tracker markers on the calibration object.

    Returns:
        numpy.ndarray: Expected positions of electromagnetic tracker markers on the calibration object.
    """
    #compute transformation FD
    DjSet = PointSet(Dj)
    djSet = PointSet(dj)
    R_D, p_D = djSet.find_registration(DjSet)
    FD = transform_from(R_D, p_D)
    


    #compute transformation FA
    AjSet = PointSet(Aj)
    ajSet = PointSet(aj)
    R_A, p_A = ajSet.find_registration(AjSet)
    FA = transform_from(R_A, p_A)

    #compute Ci expected 
    FDFA = np.dot(np.linalg.inv(FD), FA)

    cj_4d = []
    for i in range(len(cj)):
        cj_4d.append([])
        for val in cj[i]:
            cj_4d[i].append(val)
        cj_4d[i].append(1)
    
    cjt = np.transpose(cj_4d)


    CiExpected = np.dot(FDFA, cjt)

    CiExpected = np.delete(CiExpected, 3, axis=0)

    CiExpected = np.transpose(CiExpected)
    #output Ci expected 
    return CiExpected
   
