from point import Point
import pandas as pd

class CTFiducials:
    """A class for working with CT Fiducials data.

    This class allows you to read and process EM Nav data from a file.

    Attributes:
        numFrames (int): The number of frames in the EM Nav data.
        b (list of Point): A list containing Point objects representing the fiducial positions.
        bArray (list of list): A list of lists containing the fiducial positions.
    """ 
    numFrames = 0
    b = []
    bArray = []

    def __init__(self, folder, name):
        """Initialize EM Nav object.

        Args:
            folder (str): The folder path where EM Fiducials data is located.
            name (str): The name of the EM Fiducials data file.
        """      
        self.fileExtension = '-ct-fiducials.txt'
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

            self.numFiducials = map(int, vals)

       
            for i in range(self.numFiducials):
                p = Point(x_coors[i], y_coors[i], z_coors[i])
                self.b.append(p)
                self.bArray.append(p.to_array())



