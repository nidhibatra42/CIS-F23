import numpy as np

def pivot_calibration(Gj):
    #Find Go
    Go = np.mean(Gj)
    #find gj
    gj = Gj - Go
    #Find transformation Fk 
    Fk = np.dot(Gj, np.linalg.inv(gj))
    


