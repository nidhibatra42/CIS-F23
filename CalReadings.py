from point import Point
import pandas as pd
import numpy as np

class CalReadings:
    """_summary_
    """

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

        with open(self.fileName, 'r') as file:
            firstLine = file.readline().strip()
            vals = firstLine.split(',')
            
            for val in vals:
                val.strip()
            
            vals.pop()
            self.numBaseMarkers, self.numOptCalMarkers, self.numEMCalMarkers, self.numFrames = map(int, vals)
    
        totalItemsPerFrame = self.numBaseMarkers + self.numOptCalMarkers + self.numEMCalMarkers
        
        self.d = []
        self.a = []
        self.c = []

        for i in range(self.numFrames):
            self.d.append([])
            self.a.append([])
            self.c.append([])
            for j in range(totalItemsPerFrame):
                p = Point(x_coors[i * totalItemsPerFrame + j], y_coors[i * totalItemsPerFrame + j], z_coors[i * totalItemsPerFrame + j])
                if j < self.numBaseMarkers:
                    self.d[i].append(p)
                elif j < self.numBaseMarkers + self.numOptCalMarkers:
                    self.a[i].append(p)
                else:
                    self.c[i].append(p)




        








        



