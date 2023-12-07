import numpy as np
from pytransform3d.transformations import transform_from, transform
from pointSet import PointSet
from findClosestPoint import find_closest_point_slow

def estimate_F_reg(mesh, d_k, tol=1e-6, maxIterations = 100):
    F_reg = np.identity(4)
    
    for i in range(maxIterations):
        s_k = []

        #Compute sample points
        for point in d_k:
            point4d = np.append(point, 1)
            s_k.append(transform(F_reg, point4d))

        #Find closest points on the mesh
        c_k = []
        for point in s_k:
            c_k.append(find_closest_point_slow(point, mesh))

        #Make new F_reg estimate
        s_k_set = PointSet(s_k)
        d_k_set = PointSet(d_k)
        R_new, p_new = d_k_set.find_registration(s_k_set)
        F_reg_new = transform_from(R_new, p_new)

        #Check for convergence
        if np.linalg.norm(F_reg_new - F_reg) < tol:
            break

        #Update F_reg for the next iteration
        F_reg = F_reg_new

        i += 1
    
    return F_reg

