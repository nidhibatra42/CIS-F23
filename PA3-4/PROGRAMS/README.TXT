# CIS-F23
Hannah Puhov and Nidhi Batra

Programming Assignment #4

To run the program open the folder called dist. There you will see the main4 application. Open this, wait for the cue,  and type in the input file prefix. The output file will be generated and the main will quit. To run the program with a file that was not included with the student data, please add that file to the "2023 PA345 Student Data" folder.

main4.py - This is the main executable for assignment 4. It calls all the necessary functions to run through the steps outlined in the assignment to output the tip locations at each frame in tracker coordinates after iterating through various F_reg to find the best one. Main generates all objects of the file io classes

The following classes have a function to set up the data as described in the class description:
  mesh class - This class allows you to read and process the mesh file and stores it in arrays (one of all vertices, one of all triangles and neighbors).

  body class - This reads in the body A and B and store them as objects with LED markers in an array and the tip as a separate attribute

  sampleReadings class - This class allows you to read and process tracker readings of body A and B and store them in corresponding arrays

  pa3Output class - This class writes the output data to the corresponding file in the output folder

The following files contain the necessary methods to find the closest point:
  findClosestPointTriangle.py finds the closest point on or within a triangle to given point a using barycentric coordinates. Helper functions are all in this file, and called from the find_closest_point() method.

  findClosestPoint.py has a slow and fast method. The slow method iterates through each triangle in the mesh, while the fast method uses bounding spheres to decrease search time.

  boundingSpheres.py creates a bounding sphere with a specific radius and diameter that perfectly encapsulates a triangle in 3D soave.

  findDks.py contains the method to find the tip of body B in tracker coordinates using body A and sampleReadings data, and frame transformations made between them.

  FregIteration iterates through all of the closest points to d_ks and finds a registration method to get from d_k to c_k. It then repeats this process to find a better Freg until it converges or 15 trials have been run.

From Programming Assignment #1:

Point.py- This class works to transform a point to a list representation and that representation back to a point. 

pointSet.py- This is a class we wrote to perform point set registration and contains our 3D registration algorithim for question 2. 

meanPoint.py - We wrote this method to compute the midpoint of the vectors. 
