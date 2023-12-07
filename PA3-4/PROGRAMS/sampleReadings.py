import pandas as pd
from point import Point

class SampleReadings:
    
    def __init__(self, folder, name, problem, aMarks, bMarks):
        """Initialize a CalBody instance.

        Args:
            folder (str): The folder containing sample readings files.
            name (str): The name of the sample readings file.
            problem (int): the problem number (3 or 4)
            aMarks (int) the number of LED markers on body A
            bMarks(int) the number of LED markers on body B
        """      
        self.fileExtension = 'PA' + str(problem) + '-' + name + '-SampleReadingsTest.txt'
        self.fileName =  folder + '/' + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=',', skiprows=[0], names=['x', 'y', 'z'])
        self.aMarks = aMarks
        self.bMarks = bMarks
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

        #Read in the first line, which contains information about the frames
        with open(self.fileName, 'r') as file:
            firstLine = file.readline().strip()
            vals = firstLine.split(',')
            
            #Remove whitespace
            for val in vals:
                val.strip()
            
            #Remove the filename
            vals.pop()
            
            self.numMarkers, self.numFrames = map(int, vals)

        self.aArray = []
        self.bArray = []
        for k in range(self.numFrames):
            self.aArray.append([])
            self.bArray.append([])
            for i in range(self.numMarkers):
                p = Point(x_coors[k * self.numMarkers + i], y_coors[k * self.numMarkers + i], z_coors[k * self.numMarkers + i])
                if i < self.aMarks:
                    self.aArray[k].append(p.to_array())
                elif i < self.aMarks + self.bMarks:
                    self.bArray[k].append(p.to_array())
                #Skip the dummy markers

        
    
   


        



