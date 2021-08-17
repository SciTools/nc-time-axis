"""Unit tests for the `nc_time_axis.AutoCFTimeFormatter` class."""

import unittest
import unittest.mock as mock

import pytest

from nc_time_axis import AutoCFTimeFormatter, NetCDFTimeDateFormatter


class Test_pick_format(unittest.TestCase):
    def check(self, resolution):
        locator = mock.MagicMock()
        formatter = AutoCFTimeFormatter(locator, "360_day")
        return formatter.pick_format(resolution)

    def test(self):
        self.assertEqual(self.check("SECONDLY"), "%H:%M:%S")
        self.assertEqual(self.check("MINUTELY"), "%H:%M")
        self.assertEqual(self.check("HOURLY"), "%Y-%m-%d %H:%M")
        self.assertEqual(self.check("DAILY"), "%Y-%m-%d")
        self.assertEqual(self.check("MONTHLY"), "%Y-%m")
        self.assertEqual(self.check("YEARLY"), "%Y")


def test_NetCDFTimeDateFormatter_warning():
    locator = mock.MagicMock()
    with pytest.warns(FutureWarning, match="AutoCFTimeFormatter"):
        NetCDFTimeDateFormatter(locator, "360_day", "days since 2000-01-01")


def test_NetCDFTimeDateFormatter_time_units_warning():
    locator = mock.MagicMock()
    with pytest.warns(DeprecationWarning, match="time_units"):
        NetCDFTimeDateFormatter(locator, "360_day", "days since 2000-01-01")


if __name__ == "__main__":
    unittest.main()
