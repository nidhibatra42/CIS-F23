# CIS-F23
Hannah Puhov and Nidhi Batra
Programming Assignment #1 

To run the program open the folder called dist. There you will see the main application. Open this, wait for the cue,  and type in the input file prefix. The output file will be generated and the main will quit. To run the program with a file that was not included with the student data, please add that file to the "PA1 Student Data" folder.

main.py - This is how our program is executed. In this file, the name of the folder and file name are specified according to which set of data you chose to run. The appropriate methods (problems 4, 5, and 6) are called to create our output file with the data we generate. 

CalReadings.py -  This class reads calibration data from a specified file, processes it, and organizes it into
three different lists based on marker types (Base Markers, OptCal Markers, and EMCal Markers).

EMPivot.py- This is a class we wrote for processing EM pivot data. 

OptPivot.py- This is a class we wrote for processing optical tracking data. 

OutputWriter.py - This class writes the output data to a text file. 

Point.py- This class works to transform a point to a list representation and that representation back to a point. 

calBody.py - This represents the calibration object and sets up the data from the file in the correct format for us to use. 

emPivotCalibration.py - This is the main method used for performing a pivot calibration for the EM probe and determining the position relative to the EM tracker base coordinate system of the dimple in the calibration post as outlined in problem 5. Calls pivotCalibration methods.

expectedValues.py - This is the method we wrote for question 4 and it finds the expected positions of markers on the calibration object as outlined in the problem. 

optPivotCalibration.py - This is the method we wrote for question 6 to perform optical pivot calibration and determine the position of the dimple.

pivotCalibration.py - This has the method that creates the baseline for least squares regression, as well as the method written for question 3 to implement pivot calibration on a more general level. 

pointSet.py- This is a class we wrote to perform point set registration and contains our 3D registration algorithim for question 2. 

testPivotCalibration.py - This is test method written to test our pivot calibration method in question 3.

testRegistration.py - This is a test method written to test our registration method written in question 2.

test_Point.py - This is a test written to test our point class we wrote to help use the package we found in question 1 with the way we wanted to format our data for processing. 

meanPoint.py - We wrote this method to compute the midpoint of the vectors. 
