# CIS-F23
Hannah Puhov and Nidhi Batra


Programming Assignment #2: 
We added on to the programs from assignment 1. 

main2.py - This is the main executable for assignment 2. It calls all the necessary functions to run through the steps outlined in the assignment to output the tip location with respect to CT coordinates. 

CTfiducials class - This class allows you to read and process fiducial coordinate data from a file and stores it in arrays.

EMFiducials class - This reads in the EMNav fiducial and store it in the corresponding arrays

emNav class- This class allows you to read and process EM Nav data from a file storing it in an array

DistortionCorrection class - This class applies distortion correction to the set of points 
  function create_scale_box - creates a box that the values will fit inside when scaled 
  function scale_to_box - scales the points to fit inside the box made in the previous function
  function single_coor_bernstein - Calculate a single coordinate of the Bernstein polynomial for      distortion correction.
  function get_ci_expecteds - Calculate and store expected values for ci.
  function create_F - Create a matrix F for distortion correction based on scaled points and frame.
  function create_f_row - Create a row in the matrix F using a scaled point and the single            coordinate Bernstein.
  function generate_distortion_correction - Generate distortion correction matrices for each frame.

Programming Assignment #1:

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
