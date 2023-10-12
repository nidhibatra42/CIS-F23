from point import Point
import pandas as pd
import numpy as np

class CalReadings:
    """A class for reading calibration data from a file and organizing it.

    This class reads calibration data from a specified file, processes it, and organizes it into
    three different lists based on marker types (Base Markers, OptCal Markers, and EMCal Markers).

    Attributes:
        fileExtension (str): The file extension for calibration data files.
        fileName (str): The full path to the calibration data file.
        data (pd.DataFrame): A pandas DataFrame containing the calibration data.
        numBaseMarkers (int): The number of Base Markers in the data.
        numOptCalMarkers (int): The number of OptCal Markers in the data.
        numEMCalMarkers (int): The number of EMCal Markers in the data.
        numFrames (int): The total number of frames in the data.

    Methods:
        data_setup(): Process the data and organize it into lists of Point objects.

    Args:
        folder (str): The folder where the calibration data file is located.
        name (str): The name of the calibration data file.
    """
    
    def __init__(self, folder, name):
        """Initialize the CalReadings object with folder and name.

        Args:
            folder (str): The folder where the calibration data file is located.
            name (str): The name of the calibration data file.
        """       
        self.fileExtension = '-calreadings.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Process the calibration data and organize it into lists of Point objects.

        This method processes the data, extracts relevant information, and organizes the data into
        separate lists for Base Markers, OptCal Markers, and EMCal Markers.

        Returns:
            None
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




        








        



