import pandas as pd
from point import Point

class Body:
    
    def __init__(self, folder, problem, body):
        """Initialize a CalBody instance.

        Args:
            folder (str): The folder containing body data files.
            problem (int): the problem number (3 or 4)
            body (str): 'A' or 'B', the body type
        """      
        self.fileExtension = 'Problem' + str(problem) + '-Body' + body + '.txt'
        self.fileName =  folder + '/' + self.fileExtension
        self.data = pd.read_csv(self.fileName, delim_whitespace=True, skiprows=[0], names=['x', 'y', 'z'])
        self.data_setup()

    def data_setup(self):
        """Process the data body and organize it into lists of Point objects.

        This method processes the data, extracts relevant information, and organizes the data into
        a list of markers LEDs and one pivot location

        Returns:
            None
        """  
        #Pandas inherently skips the first line, due to treating
        #it as a title, so we can call the coordinates as the entire range of rows 
        x_coors = self.data['x']
        y_coors = self.data['y']
        z_coors = self.data['z']

        self.numMarkers = len(x_coors) - 1 #since the last line is the tip location

        self.yArray = []
        for i in range(self.numMarkers):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            self.yArray.append(p.to_array())

        tipIndex = self.numMarkers
        tip = Point(x_coors[tipIndex], y_coors[tipIndex], z_coors[tipIndex])
        self.tip = tip.to_array()

        
    
   


        



