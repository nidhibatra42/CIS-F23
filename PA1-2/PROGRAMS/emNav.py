from point import Point
import pandas as pd

class EMNav:
    """A class for working with EM Nav data.

    This class allows you to read and process EM Nav data from a file.

    Attributes:
        numFrames (int): The number of frames in the EM Nav data.
        g (list of list of Point): A list of lists containing Point objects representing the marker positions for each frame.
        gArray (list of list of list): A list of lists of lists containing the marker positions as arrays for each frame.
    """ 
    numFrames = 0
    g = []
    GArray = []

    def __init__(self, folder, name):
        """Initialize EM Nav object.

        Args:
            folder (str): The folder path where EMPivot data is located.
            name (str): The name of the EMPivot data file.
        """      
        self.fileExtension = '-em-nav.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Read in the EMNav data and store it in the corresponding arrays
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

            self.numProbeMarkers, self.numFrames = map(int, vals)

        for i in range(self.numFrames):
            self.g.append([])
            self.GArray.append([])
            for j in range(self.numProbeMarkers):
                p = Point(x_coors[i * self.numProbeMarkers + j], y_coors[i * self.numProbeMarkers + j], z_coors[i * self.numProbeMarkers + j])
                self.g[i].append(p)
                self.GArray[i].append(p.to_array())



