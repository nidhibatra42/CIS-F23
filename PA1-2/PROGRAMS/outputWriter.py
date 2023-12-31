import os

class OutputWriter:
    """Class for writing output data to a text file."""
    def __init__(self, folder, name, numCalMarkers, numFrames):
        """Initialize the OutputWriter.

        Args:
            folder (str): The folder path where the output file will be saved.
            name (str): The name of the output file.
            numCalMarkers (int): The number of calibration markers.
            numFrames (int): The total number of frames in the output.
        """       
        self.fileExtension = '-output1.txt'
        self.fileName =  folder + '/' + name + self.fileExtension

        if not os.path.exists(folder):
             os.makedirs(folder)

        with open(self.fileName, 'w') as output:
            line1 = f"{numCalMarkers}, {numFrames}, {name + self.fileExtension}\n"
            output.write(line1)
            output.close()
        
    
    def add_frame(self, ci):
        """Add a frame to the output file.

        Args:
            ci (list): A list of points representing the frame data.
        """
        with open(self.fileName, 'a') as output:
            for point in ci:
                rounded_point = [round(x, 2) for x in point]
                output.write(', '.join(map(str, rounded_point)) + '\n')
            output.close()

    def add_pivot(self, pivot):
        """Add the coordinates of a pivot to the output file

        Args:
            pivot (1x3 array): coordinates of the pivot in 3D space
        """   

        with open (self.fileName, 'a') as output:
                rounded_pivot = [round(x, 2) for x in pivot]
                output.write(', '.join(map(str, rounded_pivot)) + '\n')
        output.close()  




