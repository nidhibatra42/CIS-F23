import math

def closest_point_triangle(point, verts):
    """Find the closest point on a mesh through a slow
      (iterative) approach

    Args:
        point (1x3 array): Point in search of closest point on mesh
        verts (list of 1x3 arrays): All vertices on the triangle

    Returns:
        1x3 array: Closest point on the mesh to point input
    """    
    # Make an initial guess that the closest point in the mesh
    # is the first one
    closestPoint = verts[0]
    d = dist(point, closestPoint)
    
    #Iterate through each point in the mesh and find the closest
    for vert in verts:
        d1 = dist(point, vert)

        if d1 < d:
            d = d1
            closestPoint = vert
    
    return closestPoint


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