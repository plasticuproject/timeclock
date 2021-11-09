"""Unit tests for calc_time function."""

import unittest
from timeclock import calc_time


class TestCalcTime(unittest.TestCase):
    """Unit tests for calc_time funtion"""
    def test_expected_behavior(self) -> None:
        """Expected behavior for calc_time funciton."""
        add_time = calc_time((2, 17), "1015", False, "0230", True)
        self.assertEqual(add_time, (6, 32))


if __name__ == '__main__':
    unittest.main()
