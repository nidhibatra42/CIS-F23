from point import Point
import unittest

class PointTest(unittest.TestCase):
    """Test cases for the Point class.

    Args:
        unittest (_type_): This class inherits from unittest.TestCase.
    """
    def test_point_initialized_with_zeros(self):
        """Test if a Point is correctly initialized with zeros.
        """       
        p = Point()

        self.assertEquals(p.x, 0)
        self.assertEquals(p.y, 0)
        self.assertEquals(p.z, 0)
    
    def test_point_initialized_with_parameters(self):
        """Test if a Point is correctly initialized with provided parameters.
        """        
        p = Point(1, -1, 3.5)

        self.assertEquals(p.x, 1)
        self.assertEquals(p.y, -1)
        self.assertEquals(p.z, 3.5)
    
    def test_to_array(self):
        """Test if the to_array method converts a Point to a list.
        """         
        p = Point(1, -1, 3.5)

        pArray = p.to_array()

        self.assertEquals(pArray, [1, -1, 3.5])
    
    def test_change_coordinates(self):
        """Test if the coordinates of a Point can be changed.
        """           
        p = Point(1, -1, 3.5)

        p.x = -1
        p.y = 1
        p.z = 4.7

        self.assertEquals(p.x, -1)
        self.assertEquals(p.y, 1)
        self.assertEquals(p.z, 4.7)
    
    def test_from_array(self):
        """Test if the from_array method sets Point coordinates from a list.
        """       
        p = Point()

        pArray = [1, -1, 3.5]
        p.from_array(pArray)

        self.assertEquals(p.x, 1)
        self.assertEquals(p.y, -1)
        self.assertEquals(p.z, 3.5)

if __name__ == "__main__":
    unittest.main()
