import unittest
from object_localization import map_to_angle, CALIB_P1, CALIB_P2

class TestMapToAngle(unittest.TestCase):
    def test_map_to_angle_sensor1(self):
        # Test sensor 1 calibration (CALIB_P1)
        # Test minimum value
        self.assertAlmostEqual(
            map_to_angle(CALIB_P1[0], CALIB_P1[0], CALIB_P1[1], CALIB_P1[2], CALIB_P1[3]), 
            CALIB_P1[2],  # Should map to minimum angle (180)
            msg="Minimum value should map to minimum angle"
        )
        
        # Test maximum value
        self.assertAlmostEqual(
            map_to_angle(CALIB_P1[1], CALIB_P1[0], CALIB_P1[1], CALIB_P1[2], CALIB_P1[3]), 
            CALIB_P1[3],  # Should map to maximum angle (90)
            msg="Maximum value should map to maximum angle"
        )
        
        # Test middle value
        middle_value = (CALIB_P1[0] + CALIB_P1[1]) / 2
        expected_angle = (CALIB_P1[2] + CALIB_P1[3]) / 2
        self.assertAlmostEqual(
            map_to_angle(middle_value, CALIB_P1[0], CALIB_P1[1], CALIB_P1[2], CALIB_P1[3]), 
            expected_angle,
            msg="Middle value should map to middle angle"
        )

    def test_map_to_angle_sensor2(self):
        # Test sensor 2 calibration (CALIB_P2)
        # Test minimum value
        self.assertAlmostEqual(
            map_to_angle(CALIB_P2[0], CALIB_P2[0], CALIB_P2[1], CALIB_P2[2], CALIB_P2[3]), 
            CALIB_P2[2],  # Should map to minimum angle (0)
            msg="Minimum value should map to minimum angle"
        )
        
        # Test maximum value
        self.assertAlmostEqual(
            map_to_angle(CALIB_P2[1], CALIB_P2[0], CALIB_P2[1], CALIB_P2[2], CALIB_P2[3]), 
            CALIB_P2[3],  # Should map to maximum angle (180)
            msg="Maximum value should map to maximum angle"
        )
        
        # Test middle value
        middle_value = (CALIB_P2[0] + CALIB_P2[1]) / 2
        expected_angle = (CALIB_P2[2] + CALIB_P2[3]) / 2
        self.assertAlmostEqual(
            map_to_angle(middle_value, CALIB_P2[0], CALIB_P2[1], CALIB_P2[2], CALIB_P2[3]), 
            expected_angle,
            msg="Middle value should map to middle angle"
        )

    def test_map_to_angle_interpolation(self):
        # Test interpolation at 25%, 75% points for sensor 1
        quarter_value = CALIB_P1[0] + (CALIB_P1[1] - CALIB_P1[0]) * 0.25
        quarter_angle = CALIB_P1[2] + (CALIB_P1[3] - CALIB_P1[2]) * 0.25
        self.assertAlmostEqual(
            map_to_angle(quarter_value, CALIB_P1[0], CALIB_P1[1], CALIB_P1[2], CALIB_P1[3]),
            quarter_angle,
            places=2,
            msg="25% value should map to 25% angle"
        )

        three_quarter_value = CALIB_P1[0] + (CALIB_P1[1] - CALIB_P1[0]) * 0.75
        three_quarter_angle = CALIB_P1[2] + (CALIB_P1[3] - CALIB_P1[2]) * 0.75
        self.assertAlmostEqual(
            map_to_angle(three_quarter_value, CALIB_P1[0], CALIB_P1[1], CALIB_P1[2], CALIB_P1[3]),
            three_quarter_angle,
            places=2,
            msg="75% value should map to 75% angle"
        )

if __name__ == '__main__':
    unittest.main()