import os
from calBody import CalBody
from calReadings import CalReadings
from emPivot import EMPivot
from emPivotCalibration import em_pivot_calibration
from optPivot import OptPivot
from optPivotCalibration import opt_pivot_calibration
from outputWriter import OutputWriter
from expectedValues import expected_values



# Get the current working directory (with the exe)
currentFolder = os.getcwd()

# Navigate up one level (parent directory with all other relevant folders)
parentFolder = os.path.dirname(currentFolder)

inputFolder = "PA1 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)

fileName = input("Enter the file prefix (i.e. pa1-debug-a): ")

calObj = CalBody(inputFolder, fileName)
calRead = CalReadings(inputFolder, fileName)
empiv = EMPivot(inputFolder, fileName)
optpiv = OptPivot(inputFolder, fileName)

outputWriter = OutputWriter(outputFolder, fileName, calObj.numEMCalMarkers, calRead.numFrames)

outputWriter.add_pivot(em_pivot_calibration(empiv))

outputWriter.add_pivot(opt_pivot_calibration(optpiv, calObj))

for i in range(calRead.numFrames):
    
    outputWriter.add_frame(expected_values(calRead.dArray[i], calRead.aArray[i], calObj.dArray, calObj.aArray, calObj.cArray))
    

    
    
    



