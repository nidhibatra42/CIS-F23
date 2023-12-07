import os
import numpy as np
from pytransform3d.transformations import transform
from body import Body
from mesh import Mesh
from sampleReadings import SampleReadings
from pa34Output import PA34Output
from kdTree import KDTree
from findDk import find_dks
from findClosestPoint import find_closest_point_slow, dist
from fregIteration import estimate_F_reg

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
bodyA = Body(inputFolder, 4, 'A')
bodyB = Body(inputFolder, 4, 'B')
sReads = SampleReadings(inputFolder, fileName, 4, bodyA.numMarkers, bodyB.numMarkers)
mesh = Mesh(inputFolder, 4)
output = PA34Output(outputFolder, fileName, sReads.numFrames, 4)

dks = find_dks(bodyA, bodyB, sReads)

#SLOW
cks = []
for point in dks:
    cks.append(find_closest_point_slow(point, mesh))
   
"""
#FAST
tree = KDTree(mesh)
for point in dks:
    ck = tree.find_closest_point_fast(point)
    record = [point[0], point[1], point[2], ck[0], ck[1], ck[2], dist(point, ck)]
    output.add_record(record)
"""

F_reg = estimate_F_reg(mesh, dks)

for i in range(len(dks)):
    point4d = np.append(dks[i], 1)
    sk = transform(F_reg, dks[i])[:3]
    record = [sk[0], sk[1], sk[2], cks[i][0], cks[i][1], cks[i][2], dist(sk, cks[i]) ]
    output.add_record(record)