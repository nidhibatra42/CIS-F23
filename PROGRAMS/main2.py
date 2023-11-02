from scaleBox import BoxScale
import os

currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)

inputFolder = "PA2 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)

prog = BoxScale('pa2-debug-a', inputFolder, outputFolder)

prog.create_scale_box()
prog.get_ci_expecteds()
prog.generate_distortion_correction()
prog.p5_2()
prog.p6_2()