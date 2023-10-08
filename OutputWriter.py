
class OutputWriter:

    def __init__(self, folder, name, numCalMarkers, numFrames):
        self.fileExtension = '-output1.txt'
        self.fileName =  folder + '/' + name + self.fileExtension

        with open(self.fileName, 'w') as output:
            line1 = f"{numCalMarkers}, {numFrames}, {name + self.fileExtension}\n"
            output.write(line1)
            output.close()
            print(line1)
        
    
    def add_frame(self, ci):

        with open (self.fileName, 'a') as output:
            for point in ci:
                output.write(', '.join(map(str, point)) + '\n')
            output.close()

   




