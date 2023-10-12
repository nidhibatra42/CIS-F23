# CIS-F23
Hannah Puhov and Nidhi Batra
Programming Assignment #1 

main.py - This is how our program is executed. In this file, the name of the folder and file name are specified according to which set of data you chose to run. The appropriate methods (problems 4, 5, and 6) are called to create our output file with the data we generate. 

CalReadings.py -  This class reads calibration data from a specified file, processes it, and organizes it into
three different lists based on marker types (Base Markers, OptCal Markers, and EMCal Markers).

EMPivot.py- This is a class we wrote for processing EM pivot data. 

OptPivot.py- This is a class we wrote for processing optical tracking data. 

OutputWriter.py - This class writes the output data to a text file. 

Point.py- This class works to transform a point to a list representation and that representation back to a point. 

calBody.py - This represents the calibration object and sets up the data from the file in the correct format for us to use. 

emPivotCalibration.py - This is the main method used for performing a pivot calibration for the EM probe and determining the position relative to the EM tracker base coordinate system of the dimple in the calibration post as outlined in problem 5. 

expectedValues.py - This is the method we wrote for question 4 and it finds the expected positions of markers on the calibration object as outlined in the problem. 

optPivotCalibration.py

pivotCalibration.py

pointSet.py

testPivotCalibration.py

testRegistration.py

test_Point.py
