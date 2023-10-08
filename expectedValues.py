import numpy as np
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
    FD = np.dot(Dj, np.linalg.inv(dj))

    #compute transformation FA
    FA = np.dot(Aj, np.linalg.inv(aj))

    #compute Ci expected 
    FDFA = np.dot(np.linalg.inv(FD), FA)
    CiExpected = np.dot(FDFA, cj)

    #output Ci expected 
    return CiExpected
   