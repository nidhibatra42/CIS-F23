from point import Point
import pandas as pd
import numpy as np

class EMPivot:
    """Class for processing EMPivot data."""
    numFrames = 0
    g = [[]]

    def __init__(self, folder, name):
        """Initialize EMPivot object.

        Args:
            folder (str): The folder path where EMPivot data is located.
            name (str): The name of the EMPivot data file.
        """      
        self.fileExtension = '-empivot.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Setup data from the text file."""        
        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        self.numProbeMarkers = int(self.data.columns[0])
        self.numFrames = int(self.data.columns[1])
     
        self.g = []

        for i in range(self.numFrames):
            self.g.append([])
            for j in range(self.numProbeMarkers):
                p = Point(x_coors[i * self.numProbeMarkers + j], y_coors[i * self.numProbeMarkers + j], z_coors[i * self.numProbeMarkers + j])
                self.g[i].append(p)

        self.array_setup()

    def array_setup(self):
        """Setup an array for EMPivot data."""    
        self.GArray = []

        for i in range(self.numFrames):
            frame = []
            for j in range(self.numProbeMarkers):
                frame.append(self.g[i][j].to_array())
            self.GArray.append(frame)
