import Point
import unittest

class PointTest(unittest.TestCase):

    def test_point_initialized_with_zeros(self):
        p = Point()

        self.assertEquals(p.x, 0)
        self.assertEquals(p.y, 0)
        self.assertEquals(p.z, 0)
    
    def test_point_initialized_with_parameters(self):
        p = Point(1, -1, 3.5)

        self.assertEquals(p.x, 1)
        self.assertEquals(p.y, -1)
        self.assertEquals(p.z, 3.5)
    
    def test_to_array(self):
        p = Point(1, -1, 3.5)

        pArray = p.to_array()

        self.assertEquals(pArray, [1, -1, 3.5])
    
    def test_change_coordinates(self):
        p = Point(1, -1, 3.5)

        p.x = -1
        p.y = 1
        p.z = 4.7

        self.assertEquals(p.x, -1)
        self.assertEquals(p.y, 1)
        self.assertEquals(p.z, 4.7)
    
    def test_from_array(self):
        p = Point()

        pArray = [1, -1, 3.5]
        p.from_array(pArray)

        self.assertEquals(p.x, 1)
        self.assertEquals(p.y, -1)
        self.assertEquals(p.z, 3.5)

