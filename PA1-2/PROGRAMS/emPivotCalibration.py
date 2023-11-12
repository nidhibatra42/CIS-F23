import pivotCalibration as pivotCalibration

def em_pivot_calibration(emPivot):
    """Perform EM pivot calibration.

    Args:
        emPivot (EMPivot): An instance of the EMPivot class.
    """        
    Gj = emPivot.GArray

    return pivotCalibration.pivot_calibration(Gj, emPivot.numFrames, emPivot.numProbeMarkers)