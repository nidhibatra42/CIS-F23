
class OutputWriter:
    """_summary_
    """
    def __init__(self, folder, name, numCalMarkers, numFrames):
        """_summary_

        Args:
            folder (_type_): _description_
            name (_type_): _description_
            numCalMarkers (_type_): _description_
            numFrames (_type_): _description_
        """        
        self.fileExtension = '-output1.txt'
        self.fileName =  folder + '/' + name + self.fileExtension

        with open(self.fileName, 'w') as output:
            line1 = f"{numCalMarkers}, {numFrames}, {name + self.fileExtension}\n"
            output.write(line1)
            output.close()
            print(line1)
        
    
    def add_frame(self, ci):
        """_summary_

        Args:
            ci (_type_): _description_
        """
        with open (self.fileName, 'a') as output:
            for point in ci:
                output.write(', '.join(map(str, point)) + '\n')
            output.close()

   




