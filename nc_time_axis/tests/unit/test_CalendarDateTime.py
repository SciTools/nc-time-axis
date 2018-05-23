"""Unit tests for the `nc-time-axis.CalendarDateTime` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import cftime

from nc_time_axis import CalendarDateTime


class Test___eq__(unittest.TestCase):
    def setUp(self):
        self.cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6),
                                    '360_day')

    def test_equal(self):
        self.assertTrue(self.cdt == self.cdt)

    def test_diff_cal(self):
        other_cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6),
                                     '365_day')
        self.assertFalse(self.cdt == other_cdt)

    def test_diff_datetime(self):
        other_cdt = CalendarDateTime(cftime.datetime(1992, 11, 23, 3, 6),
                                     '360_day')
        self.assertFalse(self.cdt == other_cdt)

    def test_diff_type(self):
        self.assertFalse(self.cdt == 'not a CalendarDateTime')


class Test__ne__(unittest.TestCase):
    def setUp(self):
        self.cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6),
                                    '360_day')

    def test_equal(self):
        self.assertFalse(self.cdt != self.cdt)

    def test_diff_cal(self):
        other_cdt = CalendarDateTime(cftime.datetime(1967, 7, 22, 3, 6),
                                     '365_day')
        self.assertTrue(self.cdt != other_cdt)

    def test_diff_datetime(self):
        other_cdt = CalendarDateTime(cftime.datetime(1992, 11, 23, 3, 6),
                                     '360_day')
        self.assertTrue(self.cdt != other_cdt)

    def test_diff_type(self):
        self.assertTrue(self.cdt != 'not a CalendarDateTime')


if __name__ == "__main__":
    unittest.main()
