class Point:
    """_summary_
    """    
    def __init__(self, x = 0, y = 0, z = 0):
        """_summary_

        Args:
            x (int, optional): _description_. Defaults to 0.
            y (int, optional): _description_. Defaults to 0.
            z (int, optional): _description_. Defaults to 0.
        """        
        self.x = x
        self.y = y
        self.z = z
    
    def to_array(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return [self.x, self.y, self.z]
    
    def from_array(self, pointArray):
        """_summary_

        Args:
            pointArray (_type_): _description_
        """        
        self.x = pointArray[0]
        self.y = pointArray[1]
        self.z = pointArray[2]

    

