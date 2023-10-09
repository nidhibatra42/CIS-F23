from point import Point
import pandas as pd
import numpy as np

class CalReadings:
    """_summary_
    """
    numBaseMarkers = 0
    numOptCalMarkers = 0
    numEMCalMarkers = 0
    numFrames = 0

    d = [[]]
    a = [[]]
    c = [[]]

    def __init__(self, folder, name):
        """_summary_

        Args:
            folder (_type_): _description_
            name (_type_): _description_
        """        
        self.fileExtension = '-calreadings.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """_summary_
        """        
        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        numBaseMarkers = int(self.data.columns[0])
        numOptCalMarkers = int(self.data.columns[1])
        numEMCalMarkers = int(self.data.columns[2])
        numFrames = int(self.data.columns[3])
    
        totalItemsPerFrame = numBaseMarkers + numOptCalMarkers + numEMCalMarkers
        
        self.d = np.zeros((numFrames, totalItemsPerFrame))
        self.a = np.zeros((numFrames, totalItemsPerFrame))
        self.c = np.zeros((numFrames, totalItemsPerFrame))

        for i in range(numFrames):
            for j in range(totalItemsPerFrame):
                p = Point(x_coors[i * totalItemsPerFrame + j], y_coors[i * totalItemsPerFrame + j], z_coors[i * totalItemsPerFrame + j])
                if j < numBaseMarkers:
                    self.d[i][j] = p
                elif j < numBaseMarkers + numOptCalMarkers:
                    self.a[i][j] = p
                else:
                    self.c[i][j] = p




        



