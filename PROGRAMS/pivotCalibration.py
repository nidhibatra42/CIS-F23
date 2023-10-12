import numpy as np

def pivot_calibration(R_fks, p_fks):
   
    # Create an initial transformation matrix F_G by horizontally stacking the first rotation matrix 'R_fks[0]' with a negated identity matrix '-np.identity(3)'
    F_G = np.hstack((R_fks[0], -np.identity(3)))
    # Create a translation vector 't_g' by negating the first translation vector 'p_fks[0]'
    t_g = -1 * np.array(p_fks[0])

     # Loop through the remaining rotation and translation matrices (from index 1 to the end of the 'R_fks' and 'p_fks' lists)
    for k in range(1,len(R_fks)):
         # Horizontally stack the next rotation matrix 'R_fks[k]' with a negated identity matrix '-np.identity(3)'
        F_G = np.vstack((F_G, np.hstack((R_fks[k], -np.identity(3)))))
        # Append the negated translation vector 'p_fks[k]' to the 't_g' vector
        t_g = np.append(t_g, - p_fks[k])
    
    # Use the least-squares method to find the solution 'p_dimple' for the linear equation system represented by 'F_G' and 't_g'
    p_dimple, _, _, _ = np.linalg.lstsq(F_G, t_g, None)
    
    # Return the result 'p_dimple' after discarding the first 3 elements (which correspond to the rotational part of the transformation)
    return p_dimple[3:]
    
