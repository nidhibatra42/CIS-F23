import numpy as np
from scipy.optimize import minimize
from meanPoint import mean_point

def distance_squared(x, a, tri):
    """Get the square distance between a point "a" and 
        the barycentric coordinates of a triangle

    Args:
        x (3 x 1 array): l, u, and v
        a (1x3 array): 3d point
        tri (3x(1x3) array): 3 3d points on a triangle

    Returns:
        float: distance squared between the barycentric point and a
    """    
    l, u, v = x
    v0 = 0
    v1 = 0
    v2 = 0


    v0 = l * tri[0][0] + u * tri[1][0] + v * tri[2][0]
    v1 = l * tri[0][1] + u * tri[1][1] + v * tri[2][1]
    v2 = l * tri[0][2] + u * tri[1][2] + v * tri[2][2]


    point = [v0, v1, v2, 1]
    return np.sum((point - a)**2)

def sum_constraint(x):
    """l + u + v = 1

    Args:
        x (3x1 array): l, u, v

    Returns:
        float: sum of the array - 1
    """    
    return np.sum(x) - 1

def barycentric_formulation(a, tri):
    """find l, u, and v for barycentric find_closest_point
        between 3d point a and a triangle in 3d space

    Args:
        a (1x3 array): point to compare*
        tri (3x(1x3 array)): triangle in 3d space

    Returns:
        1x3 array: l, u, v
    """    
    guess = mean_point(tri)  # Initial guess for barycentric coordinates

    # Constraint: l + u + v = 1
    constraint = [{'type': 'eq', 'fun': sum_constraint}]

    # Minimize the squared distance function
    result = minimize(fun=distance_squared, x0=guess, args=(a, tri), constraints=constraint)

    #Return [l, u, v]
    return result.x

def project_on_segment(c, p, q):
    """project a point onto a line segment

    Args:
        c (1x3 array): point estimate
        p (1x3 array): end of line segment
        q (1x3 array): other end of line segment

    Returns:
        1x3 array: projection of point onto line segment
    """    
    c_np = np.asarray(c)
    p_np = np.asarray(p)
    q_np = np.asarray(q)

    l = np.dot((c_np - p_np), (q_np - p_np)) / np.dot((q_np - p_np), (q_np - p_np))

    l_seg = max(0, min(l, 1))

    return p_np + l_seg * (q_np - p_np)


def find_closest_point(a, tri):
    """find the closest point to a on a triangle

    Args:
        a (1x3 array): point to find nearest location
        tri (3x(1x3) array): triangle on mesh

    Returns:
        1x3 array: nearest point on the triangle to a
    """    
    #q, r, p
    bary = barycentric_formulation(a, tri)

    l = bary[0]
    u = bary[1]
    v = bary[2]

    v0 = 0
    v1 = 0
    v2 = 0


    v0 = l * tri[0][0] + u * tri[1][0] + v * tri[2][0]
    v1 = l * tri[0][1] + u * tri[1][1] + v * tri[2][1]
    v2 = l * tri[0][2] + u * tri[1][2] + v * tri[2][2]

    c = [v0, v1, v2]

    if l >= 0 and u >=0 and v >= 0:
        return c
    elif l < 0:
        return project_on_segment(c, tri[1], tri[2])
    elif u < 0:
        return project_on_segment(c, tri[2], tri[0])
    else: #v < 0
        return project_on_segment(c, tri[0], tri[1])


