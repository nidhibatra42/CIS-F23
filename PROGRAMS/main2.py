from FindingTipCT import FindingTipCT
import os

currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)

inputFolder = "PA2 Student Data"
outputFolder = "OUTPUT"

inputFolder = os.path.join(parentFolder, inputFolder)
outputFolder = os.path.join(parentFolder, outputFolder)

prog = FindingTipCT('pa2-debug-a', inputFolder, outputFolder)

prog.create_scale_box()
prog.get_ci_expecteds()
prog.generate_distortion_correction()
prog.bj_emcoords()
prog.registration_frame()
prog.tip_ct()