"""Unit tests for the `nc-time-axis.CalendarDateTime` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import netcdftime

from nc_time_axis import CalendarDateTime


class Test___eq__(unittest.TestCase):
    def test_equal(self):
        cdt = CalendarDateTime(netcdftime.datetime(1967, 7, 22, 3, 6),
                               '360_day')
        self.assertTrue(cdt.__eq__(cdt))

    def test_diff_cal(self):
        cdt = CalendarDateTime(netcdftime.datetime(1967, 7, 22, 3, 6),
                               '360_day')
        other_cdt = CalendarDateTime(netcdftime.datetime(1967, 7, 22, 3, 6),
                                     '365_day')
        self.assertFalse(cdt.__eq__(other_cdt))

    def test_diff_datetime(self):
        cdt = CalendarDateTime(netcdftime.datetime(1967, 7, 22, 3, 6),
                               '360_day')
        other_cdt = CalendarDateTime(netcdftime.datetime(1992, 11, 23, 3, 6),
                                     '360_day')
        self.assertFalse(cdt.__eq__(other_cdt))


if __name__ == "__main__":
    unittest.main()
