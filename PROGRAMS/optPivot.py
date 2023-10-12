from point import Point
import pandas as pd
import numpy as np

class OptPivot:
    """Class for processing OptPivot data."""   

    numBaseMarkers = 0
    numOptProbeMarkers = 0
    numFrames = 0

    d = [[]]
    h = [[]]

    def __init__(self, folder, name):
        """Initialize OptPivot object.

        Args:
            folder (str): The folder path where OptPivot data is located.
            name (str): The name of the OptPivot data file.
        """   
        self.fileExtension = '-optpivot.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Setup data from the text file."""
        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        self.numBaseMarkers = int(self.data.columns[0])
        self.numOptProbeMarkers = int(self.data.columns[1])
        self.numFrames = int(self.data.columns[2])
    
        totalItemsPerFrame = self.numBaseMarkers + self.numOptProbeMarkers
        
        self.d = []
        self.h = []
        self.DArray = []
        self.HArray = []
       
        for i in range(self.numFrames):
            self.d.append([])
            self.h.append([])
            self.DArray.append([])
            self.HArray.append([])
            for j in range(totalItemsPerFrame):
                p = Point(x_coors[i * totalItemsPerFrame + j], y_coors[i * totalItemsPerFrame + j], z_coors[i * totalItemsPerFrame + j])
                if j < self.numBaseMarkers:
                    self.d[i].append(p)
                    self.DArray[i].append(p.to_array())
                else:
                    self.h[i].append(p)
                    self.HArray[i].append(p.to_array())
        




        


