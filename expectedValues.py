import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
from outputWriter import OutputWriter

def expected_values(Dj, Aj, dj, aj, cj):
    """_summary_

    Args:
        Dj (_type_): _description_
        Aj (_type_): _description_
        Cj (_type_): _description_
        dj (_type_): _description_
        aj (_type_): _description_
        cj (_type_): _description_

    Returns:
        _type_: _description_
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
   
