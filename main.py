from calBody import CalBody
from calReadings import CalReadings
from emPivot import EMPivot
from emPivotCalibration import em_pivot_calibration
from optPivot import OptPivot
from optPivotCalibration import opt_pivot_calibration
from outputWriter import OutputWriter
from expectedValues import expected_values

inputFolder = "PA1 Student Data"
outputFolder = "OUTPUT"

fileName = input("Enter the file prefix (i.e. pa1-debug-a): ")

calObj = CalBody(inputFolder, fileName)
calRead = CalReadings(inputFolder, fileName)
empiv = EMPivot(inputFolder, fileName)
optpiv = OptPivot(inputFolder, fileName)

outputWriter = OutputWriter(outputFolder, fileName, calObj.numEMCalMarkers, calRead.numFrames)

outputWriter.add_pivot(em_pivot_calibration(empiv))

outputWriter.add_pivot(opt_pivot_calibration(optpiv, calObj))

for i in range(calRead.numFrames):
    DPoints = calRead.d[i]
    APoints = calRead.a[i]

    DArray = []
    AArray = []

    for j in range(len(DPoints)):
        DArray.append(DPoints[j].to_array())
    
    for j in range(len(APoints)):
        AArray.append(APoints[j].to_array())
    
    outputWriter.add_frame(expected_values(DArray, AArray, calObj.dArray, calObj.aArray, calObj.cArray))
    

    
    
    



