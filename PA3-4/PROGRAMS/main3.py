import os
from body import Body
from mesh import Mesh
from sampleReadings import SampleReadings
from pa34Output import PA34Output
from kdTree import KDTree
from findDk import find_dks
from findClosestPoint import find_closest_point_slow, dist

#Get all relevant directories
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)

inputFolder = "2023 PA345 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)
#Prompt for user input of filename
fileName = input("Enter the file prefix (i.e. A-Debug): ")

#Construct all the 
bodyA = Body(inputFolder, 3, 'A')
bodyB = Body(inputFolder, 3, 'B')
sReads = SampleReadings(inputFolder, fileName, 3, bodyA.numMarkers, bodyB.numMarkers)
mesh = Mesh(inputFolder, 3)
output = PA34Output(outputFolder, fileName, sReads.numFrames, 3)

dks = find_dks(bodyA, bodyB, sReads)

#SLOW


for point in dks:
    ck = find_closest_point_slow(point, mesh)
    record = [point[0], point[1], point[2], ck[0], ck[1], ck[2], dist(point, ck)]
    output.add_record(record)

"""
#FAST
tree = KDTree(mesh)
for point in dks:
    ck = tree.find_closest_point_fast(point)
    record = [point[0], point[1], point[2], ck[0], ck[1], ck[2], dist(point, ck)]
    output.add_record(record)
"""
