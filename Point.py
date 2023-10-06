class Point:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    def to_array(self):
        return [self.x, self.y, self.z]
    
    def from_array(self, pointArray):
        self.x = pointArray[0]
        self.y = pointArray[1]
        self.z = pointArray[2]

    

