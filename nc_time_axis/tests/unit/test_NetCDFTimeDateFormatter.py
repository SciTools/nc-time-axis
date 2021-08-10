"""Unit tests for the `nc-time-axis.NetCDFTimeDateFormatter` class."""

import unittest
import unittest.mock as mock

from nc_time_axis import NetCDFTimeDateFormatter


class Test_pick_format(unittest.TestCase):
    def check(self, resolution):
        locator = mock.MagicMock()
        formatter = NetCDFTimeDateFormatter(
            locator, "360_day", "days since 2000-01-01 00:00"
        )
        return formatter.pick_format(resolution)

    def test(self):
        self.assertEqual(self.check("SECONDLY"), "%H:%M:%S")
        self.assertEqual(self.check("MINUTELY"), "%H:%M")
        self.assertEqual(self.check("HOURLY"), "%Y-%m-%d %H:%M")
        self.assertEqual(self.check("DAILY"), "%Y-%m-%d")
        self.assertEqual(self.check("MONTHLY"), "%Y-%m")
        self.assertEqual(self.check("YEARLY"), "%Y")


if __name__ == "__main__":
    unittest.main()
