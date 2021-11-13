"""Unit tests for calc_time function."""

import unittest
from timeclock import calc_time


class TestCalcTime(unittest.TestCase):
    """Unit tests for calc_time funtion"""
    def test_expected_behavior(self) -> None:
        """Expected behavior for calc_time funciton."""
        add_time_one = calc_time((2, 17), "1015", False, "0230", True)
        self.assertEqual(add_time_one, (6, 32))

        add_time_two = calc_time((0, 0), "1200", False, "1200", False)
        self.assertEqual(add_time_two, (24, 0))

        add_time_three = calc_time((0, 0), "1200", True, "1200", False)
        self.assertEqual(add_time_three, (12, 0))

        add_time_four = calc_time((0, 0), "1130", True, "0200", False)
        self.assertEqual(add_time_four, (2, 30))

        add_time_five = calc_time((0, 35), "0200", True, "0235", True)
        self.assertEqual(add_time_five, (1, 10))

        add_time_five = calc_time((0, 0), "1200", True, "1215", True)
        self.assertEqual(add_time_five, (0, 15))


if __name__ == '__main__':
    unittest.main()
