import numpy as np
from meanPoint import mean_point
from pointSet import PointSet
from pytransform3d.transformations import transform, transform_from

def pivot_calibration(Xj, numFrames, numItems):
    """Calibrate a pivot point using a series of frames.

    Args:
        Xj (3D list): A list of frames, where each frame is a list of points represented as 3D coordinates.
        numFrames (int): The number of frames in the calibration dataset.
        numItems (int): The number of points in each frame.

    Returns:
        numpy.ndarray: The calibrated pivot point as a 3D vector.
    """    
    Xo = mean_point(Xj[0])

    #find xj
    xj = []
   
    #for each point
    for j in range(numItems):
        xj.append([])
        #for each coordinate in the point
        for i in range(3):
            xj[j].append(Xj[0][j][i] - Xo[i])

    xjSet = PointSet(xj)

    #Create arrays for F_G[k] and t_g[k]
    R_fks = []
    p_fks = []
    
    #Fill in the arrays
    for k in range(numFrames):
        XjSet = PointSet(Xj[k])

        R_fK, p_fK = xjSet.find_registration(XjSet)

        R_fks.append(R_fK)
        p_fks.append(p_fK)

    return find_p_dimple(R_fks, p_fks)


def find_p_dimple(R_fks, p_fks):
    """Calculate the calibrated pivot point based on rotation and translation matrices.

    Args:
        R_fks (list of 3x3 arrays): A list of rotation matrices.
        p_fks (list of 1x3 arrays): A list of translation vectors.

    Returns:
        numpy.ndarray: The calibrated pivot point as a 3D vector.
    """    
   
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
    
def get_pointer_locations(Xj, numFrames, numItems, p_dimple):
    p_dimple4D = np.append(p_dimple, 1)

    Xo = mean_point(Xj[0])

    #find xj
    xj = []

    #for each point
    for j in range(numItems):
        xj.append([])
        #for each coordinate in the point
        for i in range(3):
            xj[j].append(Xj[0][j][i] - Xo[i])

    xjSet = PointSet(xj)
    
    pointerLocations = np.empty((1, 4))
    #Fill in the arrays
    for k in range(numFrames):
        XjSet = PointSet(Xj[k])

        R_fK, p_fK = xjSet.find_registration(XjSet)
        F_k = transform_from(R_fK, p_fK)

        pointer = transform(F_k, p_dimple4D)
        pointerLocations = np.vstack((pointerLocations, pointer))
    
    return pointerLocations
    
