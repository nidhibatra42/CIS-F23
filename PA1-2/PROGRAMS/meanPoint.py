def mean_point( points):
    """Find the average point in a list of points

    Args:
        points (list of 1x3 arrays): list of points in 3D space
    """        
    mean = [0, 0, 0]

    for point in points:
        for i in range(3):
            mean[i] += point[i]
    
    for i in range(3):
        mean[i] = mean[i] / len(points)

    return mean