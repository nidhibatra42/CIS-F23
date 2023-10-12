import pandas as pd
from point import Point

class CalBody:
    """Represents a calibration object for an electromagnetic tracking system.

    Attributes:
        numBaseMarkers (int): Number of base markers on the calibration object.
        numOptCalMarkers (int): Number of optical calibration markers on the calibration object.
        numEMCalMarkers (int): Number of electromagnetic calibration markers on the calibration object.
        d (list): List to store positions on the base unit of the electromagnetic tracking system as Points.
        a (list): List to store positions of optical calibration markers as Points.
        c (list): List to store measured positions of the electromagnetic tracker markers on the calibration object as Points.
        dArray (list): List to store positions on the base unit of the electromagnetic tracking system as 1x3 arrays.
        aArray (list): List to store positions of optical calibration markers as 1x3 arrays.
        cArray (list): List to store measured positions of the electromagnetic tracker markers on the calibration object as 1x3 arrays.
   
    """
    
    numBaseMarkers = 0
    numOptCalMarkers = 0
    numEMCalMarkers = 0
    d = []
    a = []
    c = []
    dArray = []
    aArray = []
    cArray = []

    
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
        """Process the calibration data body and organize it into lists of Point objects.

        This method processes the data, extracts relevant information, and organizes the data into
        separate lists for Base Markers, OptCal Markers, and EMCal Markers.

        Returns:
            None
        """  
        #Pandas inherently skips the first line, due to treating
        #it as a title, so we can call the coordinates as the entire range of rows 
        x_coors = self.data.iloc[:,0]
        y_coors = self.data.iloc[:,1]
        z_coors = self.data.iloc[:,2]

        #Read in the first line, which contains information about the frames
        with open(self.fileName, 'r') as file:
            firstLine = file.readline().strip()
            vals = firstLine.split(',')
            
            #Remove whitespace
            for val in vals:
                val.strip()
            
            #Remove the filename
            vals.pop()

            self.numBaseMarkers, self.numOptCalMarkers, self.numEMCalMarkers = map(int, vals)
    
        totalItemsPerFrame = self.numBaseMarkers + self.numOptCalMarkers + self.numEMCalMarkers
        

        for i in range(totalItemsPerFrame):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            if i < self.numBaseMarkers:
                self.d.append(p)
                self.dArray.append(p.to_array())
            elif i < self.numBaseMarkers + self.numOptCalMarkers:
                self.a.append(p)
                self.aArray.append(p.to_array())
            else:
                self.c.append(p)
                self.cArray.append(p.to_array())
        
    
   


        



