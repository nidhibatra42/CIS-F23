class Point:
    def _init_(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def to_array(self):
        return [self.x, self.y, self.z]

    

