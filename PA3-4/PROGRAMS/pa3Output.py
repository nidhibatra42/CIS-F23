import os

class PA3Output:
    """Class for writing output data to a text file."""
    def __init__(self, folder, name, numFrames, problem):
        """Initialize the OutputWriter.

        Args:
            folder (str): The folder path where the output file will be saved.
            name (str): The name of the output file.
            numFrames (int): The total number of frames in the output.
            problem (int): problem 3 or 4
        """       
        self.fileExtension = 'PA' + str(problem) + '-' + name + '-Output.txt'
        self.fileName =  folder + '/' + self.fileExtension

        if not os.path.exists(folder):
             os.makedirs(folder)

        with open(self.fileName, 'w') as output:
            line1 = f"{numFrames}, {name + self.fileExtension}\n"
            output.write(line1)
            output.close()
        

    def add_record(self, pivot):
        """Add the coordinates of a pivot to the output file

        Args:
            pivot (1x7 array): coordinates of dk, ck in 3D space, 
            difference magnitude
        """   

        with open (self.fileName, 'a') as output:
                rounded_pivot = [round(x, 2) for x in pivot]
                output.write(', '.join(map(str, rounded_pivot)) + '\n')
        output.close()  




