from point import Point
import pandas as pd

class CTFiducials:
    """A class for working with CT Fiducials data.

    This class allows you to read and process fiducial coordinate data from a file.

    Attributes:
        numFrames (int): The number of frames in the EM Nav data.
        b (list of Point): A list containing Point objects representing the fiducial positions.
        bArray (list of list): A list of lists containing the fiducial positions.
    """ 
    numFrames = 0
    b = []
    bArray = []

    def __init__(self, folder, name):
        """Initialize CT fiducial object.

        Args:
            folder (str): The folder path where CT Fiducials data is located.
            name (str): The name of the CT Fiducials data file.
        """      
        self.fileExtension = '-ct-fiducials.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',', skiprows=[0], names=['x', 'y', 'z'])
        self.data_setup()

    def data_setup(self):
        """Read in the fiducal data and store it in the corresponding arrays
        """  
        #Pandas inherently skips the first line, due to treating
        #it as a title, so we can call the coordinates as the entire range of rows              
        x_coors = self.data['x']
        y_coors = self.data['y']
        z_coors = self.data['z']

        self.numFiducials = len(x_coors)

       
        for i in range(self.numFiducials):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            self.b.append(p)
            self.bArray.append(p.to_array())



