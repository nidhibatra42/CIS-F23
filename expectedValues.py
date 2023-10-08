import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from
from outputWriter import OutputWriter

def expected_values(Dj, Aj, Cj):
    #compute transformation between optical tracker and EM coordinates 

    #Dj
    #Find Do
    Do = np.mean(Dj)
    #find dj
    dj = Dj - Do
    #Aj
    #Find Ao
    Ao = np.mean(Aj)
    #find aj
    aj = Aj - Ao
    #Cj
    #Find Co
    Co = np.mean(Cj)
    #find cj
    cj = Cj - Co

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
   