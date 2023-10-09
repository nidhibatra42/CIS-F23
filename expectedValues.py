import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
from outputWriter import OutputWriter

def expected_values(Dj, Aj, Cj, dj, aj, cj):
    """_summary_

    Args:
        Dj (_type_): _description_
        Aj (_type_): _description_
        Cj (_type_): _description_

    Returns:
        _type_: _description_
    """    
   

    #compute transformation FD
    DjSet = PointSet(Dj)
    djSet = PointSet(dj)
    R_D, p_D = DjSet.find_registration(djSet)
    FD = transform_from(R_D, p_D)
    


    #compute transformation FA
    AjSet = PointSet(Aj)
    ajSet = PointSet(aj)
    R_A, p_A = AjSet.find_registration(ajSet)
    FA = transform_from(R_A, p_A)

    #compute Ci expected 
    FDFA = np.dot(np.linalg.inv(FD), FA)
    CiExpected = np.dot(FDFA, cj)

    #output Ci expected 
    return CiExpected
   
