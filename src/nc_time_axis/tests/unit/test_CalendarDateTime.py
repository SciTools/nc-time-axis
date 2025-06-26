"""Unit tests for the `nc-time-axis.CalendarDateTime` class."""

import unittest

import cftime
import pytest

from nc_time_axis import CalendarDateTime


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class Test___eq__(unittest.TestCase):
    def setUp(self):
        self.cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6), "360_day")

    def test_equal(self):
        self.assertTrue(self.cdt == self.cdt)

    def test_diff_cal(self):
        other_cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6), "365_day")
        self.assertFalse(self.cdt == other_cdt)

    def test_diff_datetime(self):
        other_cdt = CalendarDateTime(cftime.datetime(1992, 11, 23, 3, 6), "360_day")
        self.assertFalse(self.cdt == other_cdt)

    def test_diff_type(self):
        self.assertFalse(self.cdt == "not a CalendarDateTime")


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class Test__hash__(unittest.TestCase):
    def test(self):
        expected_datetime = cftime.datetime(1967, 7, 22, 3, 6)
        expected_calendar = "360_day"
        cdt = CalendarDateTime(expected_datetime, expected_calendar)
        expected = hash((expected_datetime, expected_calendar))
        actual = hash(cdt)
        self.assertEqual(actual, expected)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class Test__ne__(unittest.TestCase):
    def setUp(self):
        self.cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6), "360_day")

    def test_equal(self):
        self.assertFalse(self.cdt != self.cdt)

    def test_diff_cal(self):
        other_cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6), "365_day")
        self.assertTrue(self.cdt != other_cdt)

    def test_diff_datetime(self):
        other_cdt = CalendarDateTime(cftime.datetime(1992, 11, 23, 3, 6), "360_day")
        self.assertTrue(self.cdt != other_cdt)

    def test_diff_type(self):
        self.assertTrue(self.cdt != "not a CalendarDateTime")


def test_CalendarDateTime_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        CalendarDateTime(cftime.datetime(2000, 1, 1), "gregorian")


if __name__ == "__main__":
    unittest.main()
