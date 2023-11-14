import pandas as pd
from point import Point

class Mesh:
    
    def __init__(self, folder, problem):
        """Initialize a CalBody instance.

        Args:
            folder (str): The folder containing mesh data files.
            problem (int): the problem number (3 or 4)
        """      
        self.fileExtension = 'Problem' + str(problem) + 'Mesh.sur'
        self.fileName =  folder + '/' + self.fileExtension
        self.data = pd.read_csv(self.fileName, delimiter=' ', skiprows=[0], names=['x', 'y', 'z'])
        self.data_setup()

    def data_setup(self):
        """Process the mesh and organize it into lists of Point objects.

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

        #Read in the first line, which contains the number of vertices in CT coors
        with open(self.fileName, 'r') as file:
            self.numVertices = int(file.readline().strip())

        self.vArray = []
        for i in range(self.numVertices):
            p = Point(x_coors[i], y_coors[i], z_coors[i])
            self.vArray.append(p.to_array())


        #The next line contains the number of triangles
        self.numTriangles = x_coors[self.numVertices]

        #Re-read in the data for only the triangle indices
        triData = pd.read_csv(self.fileName, delimiter=' ', skiprows=range(self.numVertices + 1), names=['i1', 'i2', 'i3', 'n1', 'n2', 'n3'] )
        i1 = triData['i1']
        i2 = triData['i2']
        i3 = triData['i3']
        n1 = triData['n1']
        n2 = triData['n2']
        n3 = triData['n3']

        #List of tuples that hold: indices of current triangle vertices,
        #indices of neighboring triangles
        self.triArray = []
        for i in range(self.numTriangles):
            tri_neighbors = ([i1[i], i2[i], i3[i]], [n1[i], n2[i], n3[i]])
            self.triArray.append(tri_neighbors)

    def get_triangle(self, index):  
        """_summary_

        Args:
            index (int): index of the triangle in the array

        Returns:
            1x3 array: vertices of the triangle
        """            
        vert_indices = self.triArray[index][0]
        v1 = self.vArray[vert_indices[0]]
        v2 = self.vArray[vert_indices[1]]
        v3 = self.vArray[vert_indices[2]]

        return [v1, v2, v3]
        
        
    
   


        



