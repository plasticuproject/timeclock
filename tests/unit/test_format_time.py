"""Unit tests for format_time function."""

import unittest
from timeclock import format_time
from timeclock import FormatError


class TestFormatTime(unittest.TestCase):
    """Unit tests for format_time funtion"""
    def test_expected_behavior(self) -> None:
        """Expected behavior for format_time funciton."""
        test_one = format_time("3")
        self.assertEqual(test_one, "0300")

        test_two = format_time("11")
        self.assertEqual(test_two, "1100")

        test_three = format_time("106")
        self.assertEqual(test_three, "0106")

        test_four = format_time("0212")
        self.assertEqual(test_four, "0212")

    def test_expected_errors(self) -> None:
        """Expected errors for format_time function."""
        self.assertRaises(FormatError, format_time, "03:12")

        self.assertRaises(FormatError, format_time, "3200")

        self.assertRaises(FormatError, format_time, "0960")


if __name__ == '__main__':
    unittest.main()
