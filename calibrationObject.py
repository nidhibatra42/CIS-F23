import pandas as pd
import Point

class CalibrationObject:

    numBaseMarkers = 0
    numOptCalMarkers = 0
    numEMCalMarkers = 0
    d = []
    a = []
    c = []

    def __init__(self, folder, name):
        self.fileExtension = '-calbody.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):

        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        numBaseMarkers = int(self.data.columns[0])
        numOptCalMarkers = int(self.data.columns[1])
        numEMCalMarkers = int(self.data.columns[2])

        for i in range(numBaseMarkers + numOptCalMarkers + numEMCalMarkers):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            if i < numBaseMarkers:
                self.d.append(p)
            elif i < numBaseMarkers + numOptCalMarkers:
                self.a.append(p)
            else:
                self.c.append(p)




        



