import os
from FindingTipCT import FindingTipCT
from distortionCorrection import DistortionCorrection
from emOutput import EMOutputWriter
from outputWriter import OutputWriter
from calBody import CalBody
from calReadings import CalReadings
from emPivot import EMPivot
from ctFiducials import CTFiducials
from emFiducials import EMFiducials
from emNav import EMNav
from optPivot import OptPivot
from optPivotCalibration import opt_pivot_calibration
from emPivotCalibration import em_pivot_calibration



currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)

inputFolder = "PA2 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)

fileName = input("Enter the file prefix (i.e. pa2-debug-a): ")

calRead = CalReadings(inputFolder, fileName)
calObj = CalBody(inputFolder, fileName)
emPivot = EMPivot(inputFolder, fileName)
ctFid = CTFiducials(inputFolder, fileName)
emFid = EMFiducials(inputFolder, fileName)
emNav = EMNav(inputFolder, fileName)
emOutput = EMOutputWriter(outputFolder, fileName, emNav.numFrames)
p1Output = OutputWriter(outputFolder, fileName, calObj.numEMCalMarkers, calRead.numFrames )
optpiv = OptPivot(inputFolder, fileName)


dist = DistortionCorrection(calRead, calObj)
dist.create_scale_box()
dist.get_ci_expecteds()
dist.generate_distortion_correction()

prog = FindingTipCT(emPivot, ctFid, emFid, emNav, emOutput, dist)
prog.find_em_ct_f_reg()
prog.find_emNav_in_ct()

p1Output.add_pivot(em_pivot_calibration(emPivot))
p1Output.add_pivot(opt_pivot_calibration(optpiv, calObj))

for k in range(calRead.numFrames):
    p1Output.add_frame(dist.ciExpected[k])