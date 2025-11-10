import unittest
import math
from object_localization import calc_position, DIST, HEIGHT

class TestCalcPosition(unittest.TestCase):
    def test_basic_positions(self):
        """Test basic known positions that can be verified by hand"""

        # Object directly first second sensor
        x, y = calc_position(90, 42)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertAlmostEqual(x, 0, places=2)
        self.assertAlmostEqual(y, 19, places=2)

        # Object directly above second sensor
        x, y = calc_position(40, 90)
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertAlmostEqual(x, DIST, places=2)
        self.assertAlmostEqual(y, 20, places=2)

        #TODO: add precise angle-measuring tests later; 
        # calculations omitted for now    

        # Object directly between sensors

        # Object in some random localization

if __name__ == '__main__':
    unittest.main()