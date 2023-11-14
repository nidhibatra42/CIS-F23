import os

#Get all relevant directories
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)

inputFolder = "2023 PA345 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)
#Prompt for user input of filename
#fileName = input("Enter the file prefix (i.e. A-Debug): ")

fileName = 'A-Debug'



