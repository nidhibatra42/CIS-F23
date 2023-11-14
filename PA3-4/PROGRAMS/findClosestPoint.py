import math
from findClosestPointTriangle import find_closest_point

def dist(a, b):
    """Find the distance between two points in 3D space
    Args:
        a (1x3 array): first point
        b (1x3 array): second point
    Returns:
        float: distance between the two points
    """    
    d = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
    return d

def find_closest_point_slow(a, mesh):
    """Find the closest point on a mesh through a slow
      (iterative) approach
    Args:
        a (1x3 array): Point in search of closest point on mesh
        mesh (list of 1x3 arrays): All vertices on the triangle
    Returns:
        1x3 array: Closest point on the mesh to point input
    """    
        
    #initial guess: closest point is the first vertex
    #of the first triangle
    p = mesh.vArray(mesh.triArray[0][0])
    d = dist(a, p)

    #Iterate through each triangle to find the closest
    for index in range(mesh.numTriangles):
        tri = mesh.get_triangle(index)

        p_cur = find_closest_point(a, tri)

        d_cur = dist(a, p_cur)

        if d_cur < d:
            d = d_cur
            p = p_cur
    
    return p