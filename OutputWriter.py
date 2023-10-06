from point import Point

class OutputWriter:

    def __init__(self, folder, name):
        self.fileExtension = '-output1.txt'
        self.fileName =  folder + '/' + name + self.fileExtension
        with open(self.fileName, 'w') as output:
            output.write('hello world')
            output.close()
        
    
    def add_frame(self, ci):
        with open(self.fileName, 'w') as output:
            output.write('add line')
            output.close()
        

   




        



