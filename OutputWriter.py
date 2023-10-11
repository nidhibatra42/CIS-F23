
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

        with open(self.fileName, 'w') as output:
            line1 = f"{numCalMarkers}, {numFrames}, {name + self.fileExtension}\n"
            output.write(line1)
            output.close()
            print(line1)
        
    
    def add_frame(self, ci):
        """Add a frame to the output file.

        Args:
            ci (list): A list of points representing the frame data.
        """
        with open (self.fileName, 'a') as output:
            for point in ci:
                output.write(', '.join(map(str, point)) + '\n')
            output.close()

   




