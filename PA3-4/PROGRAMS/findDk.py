import numpy as np
from pointSet import PointSet
from pytransform3d.transformations import transform_from


def find_dks(bodyA, bodyB, sampleRead):
    """Find the d_ks: pointer tips at the bodies in tracker coordinates

    Args:
        bodyA (Body): Body A, storing LEDs in body coordinates
        bodyB (Body): Body B, storing LEDs in body coordinates
        sampleRead (SampleReadings): Storage of readings of bodies at various frames

    Returns:
        list of 1x3 arrays: Pointer tips with respect to body B
    """    
    #Create point clouds for each body
    a_body = PointSet(bodyA.yArray)
    b_body = PointSet(bodyB.yArray)
    
    d_ks = []
    for k in range(sampleRead.numFrames):
        #For each frame, find F_a
        a_tracker = PointSet(sampleRead.aArray[k])
        R_ak, p_ak = a_body.find_registration(a_tracker)
        F_ak = transform_from(R_ak, p_ak)

        #For each frame, find F_b
        b_tracker = PointSet(sampleRead.bArray[k])
        R_bk, p_bk = b_body.find_registration(b_tracker)
        F_bk = transform_from(R_bk, p_bk)

        #Follow the formula from the assignment to find d_k and add to list
        a_tip = np.append(bodyA.tip, 1)
        d = np.linalg.multi_dot((np.linalg.inv(F_bk), F_ak, a_tip))
        d_ks.append(d)

    return d_ks



    



