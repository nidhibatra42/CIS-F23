from calBody import CalBody
from calReadings import CalReadings
from emPivot import EMPivot
from emPivotCalibration import em_pivot_calibration
from optPivot import OptPivot
from optPivotCalibration import opt_pivot_calibration
from outputWriter import OutputWriter
from expectedValues import expected_values

folder = "PA1 Student Data"
fileName = "pa1-unknown-k"

#folder = input("Enter the folder name: ")
#fileName = input("Enter the file name: ")

calObj = CalBody(folder, fileName)
calRead = CalReadings(folder, fileName)
empiv = EMPivot(folder, fileName)
optpiv = OptPivot(folder, fileName)

outputWriter = OutputWriter(folder, fileName, calObj.numBaseMarkers, calRead.numFrames)

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
    

    
    
    



