import pandas as pd
import numpy as np
import Point

class EMPivot:

    numFrames = 0
    g = [[]]

    def __init__(self, folder, name):
        self.fileExtension = '-empivot.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):

        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        numProbeMarkers = int(self.data.columns[0])
        numFrames = int(self.data.columns[1])
     
        self.g = np.zeros((numProbeMarkers, numFrames))

        for i in range(numFrames):
            for j in range(numProbeMarkers):
                p = Point(x_coors[i * numProbeMarkers + j], y_coors[i * numProbeMarkers + j], z_coors[i * numProbeMarkers + j])
                self.g[i][j] = p




        



