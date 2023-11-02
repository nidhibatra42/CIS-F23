
import unittest
from unittest.mock import Mock
from FindingTipCT import FindingTipCT  

class TestBoxScale(unittest.TestCase):
     
    def setUpClass(cls):
        # Mock external dependencies and create a BoxScale instance
        cls.mock_cal_readings = Mock()
        cls.mock_cal_body = Mock()
        cls.mock_em_pivot = Mock()

        cls.box_scale = FindingTipCT("sample_file", "sample_input_folder", "sample_output_folder")
        cls.box_scale.calRead = cls.mock_cal_readings
        cls.box_scale.calObj = cls.mock_cal_body
        cls.box_scale.emPivot = cls.mock_em_pivot

    def test_scale_to_box(self):
        # Mock maxes and mins
        self.box_scale.maxes = [[1.1, 2.1, 3.1], [4.1, 5.1, 6.1]]
        self.box_scale.mins = [[0.1, 1.1, 2.1], [3.1, 4.1, 5.1]]

        point = [1.0, 2.0, 3.0]
        frame = 0

        scaled_point = self.box_scale.scale_to_box(point, frame)

        # Define your expected result
        expected_scaled_point = [0.9, 0.9, 0.9]

        self.assertEqual(scaled_point, expected_scaled_point)

    def test_single_coor_bernstein(self):
        coor = 0.5
        i = 2

        result = self.box_scale.single_coor_bernstein(coor, i)

        # Define your expected result
        expected_result = 10.3125

        self.assertAlmostEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main(FindingTipCT)