import numpy as np
import pandas as pd
from expectedValues import expected_values
from calReadings import CalReadings
from calBody import CalBody


class BoxScale:
    
    def __init__(self, fileName, inputFolder):
        calRead = CalReadings(inputFolder, fileName)
        calObj = CalBody(inputFolder, fileName)
  
        #find actual from expected using function from assignment 1, 4 
        self.ci = []
        for i in range(calRead.numFrames):
            self.ci.add_frame(expected_values(calRead.dArray[i], calRead.aArray[i], calObj.dArray, calObj.aArray, calObj.cArray))
    



    #need to determine bounding box to scale values
    def createScaleBox(self):
        #Max and min store the maxes and mins of each data frame as [x_max_i, y_max_i, z_max_i]
        self.maxes = []
        self.mins = []
        for k in range(len(self.ci)):
            ci_df = pd.DataFrame(self.ci[k], columns=['x', 'y', 'z'])
            max = []
            max.append(ci_df.x.max)
            max.append(ci_df.y.max)
            max.append(ci_df.z.max)
            min = []
            min.append(ci_df.x.max)
            min.append(ci_df.y.max)
            min.append(ci_df.z.max)
            self.maxes.append(max)
            self.mins.append(min)
            

        
        self.ci_max_x = self.ci_df.x.max
        self.ci_min_y = self.ci.x.min()
        return (ci_current - self.ci_min_axis)/ (self.ci_max_axis - self.ci_min_axis)
    

    #This is running our distortion correction
    def distortionCorrection(self):
        String x
        us = []
        for ci_current in self.ci: 
            us.append = self.scaleBox(ci_current)
        
        #find polynomials using least squares


