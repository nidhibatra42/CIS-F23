import numpy as np
from findClosestPointTriangle import find_closest_point
from findClosestPoint import dist

class KDTree:
    def __init__(self, mesh):
        """Set up the relevant arrays and grid

        Args:
            mesh (Mesh): file with vertices and triangles
        """        
        self.vArray = mesh.vArray
        self.triArray = mesh.triArray
        self.mesh = mesh
        self.build_grid()

    def build_grid(self, gridSize=20):
        """Build a grid for the kd tree

        Args:
            gridSize (int, optional): The dimension of the grid. Defaults to 10.
        """        
        # Determine the bounding box of the mesh
        minCoords = np.min(self.vArray, axis=0)
        maxCoords = np.max(self.vArray, axis=0)

        # Calculate the size of each grid cell
        cellSize = (maxCoords - minCoords) / gridSize

        # Initialize the grid as a dictionary with cell indices as keys
        self.grid = {}
        for index, (triangle, _) in enumerate(self.triArray):
            # Determine the grid cells that the triangle intersects
            minCell = tuple((min(triangle)- minCoords) // cellSize)
            maxCell = tuple((max(triangle) - minCoords) // cellSize)

            # Populate each intersected cell with the triangle index
            for i in range(int(minCell[0]), int(maxCell[0]) + 1):
                for j in range(int(minCell[1]), int(maxCell[1]) + 1):
                    for k in range(int(minCell[2]), int(maxCell[2]) + 1):
                        cell_index = (i, j, k)
                        if cell_index not in self.grid:
                            self.grid[cell_index] = []
                        self.grid[cell_index].append(index)

    def get_grid_cell_indices(self, point):
        """Get the indices of a point in the grid

        Args:
            point (1x3 array): the point in the grid

        Returns:
            list: list of indices of the grid cell
        """        
        # Determine the grid cell indices for a given point
        minCoords = np.min(self.vArray, axis=0)
        cellSize = (max(self.vArray) - minCoords) / len(self.grid)

        indices = tuple(((point - minCoords) // cellSize).astype(int))
        return [indices]  # Return a list of cell indices for simplicity
    
    def find_closest_point_fast(self, a):
        """Find the closest point in the mesh to point a

        Args:
            a (1x3 array): point to compare

        Returns:
            1x3 array: closest point on the mesh to a
        """        
        # Determine the grid cell that 'a' belongs to
        indices = self.get_grid_cell_indices(a)

        # Retrieve triangle indices from the cell and its neighbors
        candidates = set()
        for index in indices:
            if index in self.grid:
                candidates.update(self.grid[index])

        # Initialize variables to store the closest point and its distance
        cx = None
        dis = float('inf')

        # Iterate through candidate triangles and find the closest point
        for index in candidates:
            triangle = self.mesh.get_triangle(index)
            closest_point_on_triangle = find_closest_point(a, triangle)
            curDis = dist(a, closest_point_on_triangle)

            # Update closest point if a closer one is found
            if curDis < dis:
                cx = closest_point_on_triangle
                dis = curDis

        return cx



