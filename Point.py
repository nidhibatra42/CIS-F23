class Point:
    """Class representing a 3D point in space."""  
    def __init__(self, x = 0, y = 0, z = 0):
        """Initialize a 3D point.

        Args:
            x (int, optional): The x-coordinate of the point. Defaults to 0.
            y (int, optional): The y-coordinate of the point. Defaults to 0.
            z (int, optional): The z-coordinate of the point. Defaults to 0.
        """ 
    
    def to_array(self):
        """Convert the point to a list of coordinates.

        Returns:
            list: A list containing the x, y, and z coordinates of the point.
        """ 
        return [self.x, self.y, self.z]
    
    def from_array(self, pointArray):
        """Set the point's coordinates from a list.

        Args:
            pointArray (list): A list containing the x, y, and z coordinates to set.
        """        
        self.x = pointArray[0]
        self.y = pointArray[1]
        self.z = pointArray[2]

    

