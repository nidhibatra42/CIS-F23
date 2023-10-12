from point import Point
import pandas as pd

class CalBody:
    """Represents a calibration object for an electromagnetic tracking system.

    Attributes:
        numBaseMarkers (int): Number of base markers on the calibration object.
        numOptCalMarkers (int): Number of optical calibration markers on the calibration object.
        numEMCalMarkers (int): Number of electromagnetic calibration markers on the calibration object.
        d (list): List to store positions on the base unit of the electromagnetic tracking system.
        a (list): List to store positions of optical calibration markers.
        c (list): List to store measured positions of the electromagnetic tracker markers on the calibration object.
    """
    
    numBaseMarkers = 0
    numOptCalMarkers = 0
    numEMCalMarkers = 0
    d = []
    a = []
    c = []

    
    def __init__(self, folder, name):
        """Initialize a CalBody instance.

        Args:
            folder (str): The folder containing calibration data files.
            name (str): The name of the calibration data file.
        """      
        self.fileExtension = '-calbody.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Setup calibration data from a text file.
        """
        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        self.numBaseMarkers = int(self.data.columns[0])
        self.numOptCalMarkers = int(self.data.columns[1])
        self.numEMCalMarkers = int(self.data.columns[2])

        for i in range(self.numBaseMarkers + self.numOptCalMarkers + self.numEMCalMarkers):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            if i < self.numBaseMarkers:
                self.d.append(p)
            elif i < self.numBaseMarkers + self.numOptCalMarkers:
                self.a.append(p)
            else:
                self.c.append(p)
        
        self.array_setup()
    
    def array_setup(self):
        """Setup arrays from the Point objects.
        """
        self.dArray = []
        self.aArray = []
        self.cArray = []

        for i in range(len(self.d)):
            self.dArray.append(self.d[i].to_array())
        for i in range(len(self.a)):
            self.aArray.append(self.a[i].to_array())
        for i in range(len(self.c)):
            self.cArray.append(self.c[i].to_array())
        




        



