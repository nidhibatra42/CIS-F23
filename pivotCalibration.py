import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from


def pivotCalibration(Hi, hi):
    #Hi is the uppercase or to tracker point
    #hi is the lowercase vector from tracker point to its tip
    # find transformation from tracker to tip
    HiSet = PointSet(Hi)
    hiSet = PointSet(hi)

    R_i, p_i = HiSet.find_registration(hiSet)

    
