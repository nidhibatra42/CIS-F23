from point import Point
import pandas as pd

class OptPivot:
    """Class for processing OptPivot data.

    Attributes:
        numBaseMarkers (int): The number of base markers in the optical pivot data.
        numOptProbeMarkers (int): The number of optical probe markers in the OptPivot data.
        numFrames (int): The total number of frames in the optical pivot data.
        d (list of list of Point): A list of lists containing Point objects representing base markers for each frame.
        h (list of list of Point): A list of lists containing Point objects representing optical probe markers for each frame.
        DArray (list of list of list): A list of lists of lists containing the base marker positions as arrays for each frame.
        HArray (list of list of list): A list of lists of lists containing the optical probe marker positions as arrays for each frame.
  
    Methods:
        data_setup(): Process the data and organize it into lists of Point objects.

    Args:
        folder (str): The folder where the optical pivot data file is located.
        name (str): The name of the optical pivot data file.
    """
     
    numBaseMarkers = 0
    numOptProbeMarkers = 0
    numFrames = 0

    d = []
    h = []
    DArray = []
    HArray = []

    def __init__(self, folder, name):
        """Initialize OptPivot object.

        Args:
            folder (str): The folder path where OptPivot data is located.
            name (str): The name of the OptPivot data file.
        """   
        self.fileExtension = '-optpivot.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',')
        self.data_setup()

    def data_setup(self):
        """Setup data from the text file."""

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
            
            self.numBaseMarkers, self.numOptProbeMarkers, self.numFrames = map(int, vals)
    
    
        totalItemsPerFrame = self.numBaseMarkers + self.numOptProbeMarkers
    
       
        for i in range(self.numFrames):
            self.d.append([])
            self.h.append([])
            self.DArray.append([])
            self.HArray.append([])
            for j in range(totalItemsPerFrame):
                p = Point(x_coors[i * totalItemsPerFrame + j], y_coors[i * totalItemsPerFrame + j], z_coors[i * totalItemsPerFrame + j])
                if j < self.numBaseMarkers:
                    self.d[i].append(p)
                    self.DArray[i].append(p.to_array())
                else:
                    self.h[i].append(p)
                    self.HArray[i].append(p.to_array())
        




        



