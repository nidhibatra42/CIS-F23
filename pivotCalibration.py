import numpy as np

def pivot_calibration(R_fks, p_fks):

    F_G = np.hstack((R_fks[0], -np.identity(3)))
    t_g = -1 * np.array(p_fks[0])

    for k in range(1,len(R_fks)):
        F_G = np.vstack((F_G, np.hstack((R_fks[k], -np.identity(3)))))
        t_g = np.append(t_g, - p_fks[k])
    
    p_dimple, _, _, _ = np.linalg.lstsq(F_G, t_g, None)

    return p_dimple[3:]
    
