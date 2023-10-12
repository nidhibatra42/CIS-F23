def mean_point( points):
    """_summary_

    Args:
        points (_type_): _description_
    """        
    mean = [0, 0, 0]

    for point in points:
        for i in range(3):
            mean[i] += point[i]
    
    for i in range(3):
        mean[i] = mean[i] / len(points)

    return mean