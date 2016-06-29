"""Unit tests for the `nc-time-axis.NetCDFTimeConverter` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import netcdftime
import numpy as np

from nc_time_axis import NetCDFTimeConverter, CalendarDateTime


class Test_axisinfo(unittest.TestCase):
    def test_axis_default_limits(self):
        cal = '360_day'
        unit = (cal, 'days since 2000-02-25 00:00:00')
        result = NetCDFTimeConverter().axisinfo(unit, None)
        expected_dt = [netcdftime.datetime(2000, 1, 1),
                       netcdftime.datetime(2010, 1, 1)]
        np.testing.assert_array_equal(
            [cal_dt.datetime for cal_dt in result.default_limits],
            expected_dt)
        np.testing.assert_array_equal(
            [cal_dt.calendar for cal_dt in result.default_limits],
            [cal, cal])


class Test_default_units(unittest.TestCase):
    def test_360_day_calendar(self):
        calendar = '360_day'
        unit = 'days since 2000-01-01'
        val = [CalendarDateTime(netcdftime.datetime(2014, 8, 12), calendar)]
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit))


class Test_convert(unittest.TestCase):
    def test_numpy_array(self):
        val = np.array([7])
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    def test_numeric(self):
        val = 4
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    def test_numeric_iterable(self):
        val = [12, 18]
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    def test_netcdftime(self):
        val = CalendarDateTime(netcdftime.datetime(2014, 8, 12), '365_day')
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, 5333.)

    def test_netcdftime_np_array(self):
        val = np.array([CalendarDateTime(netcdftime.datetime(2012, 6, 4),
                                         '360_day')], dtype=np.object)
        result = NetCDFTimeConverter().convert(val, None, None)
        self.assertEqual(result, np.array([4473.]))

    def test_non_netcdftime_datetime(self):
        val = CalendarDateTime(4, '360_day')
        msg = 'The datetime attribute of the CalendarDateTime object must ' \
              'be of type `netcdftime.datetime`.'
        with self.assertRaisesRegexp(ValueError, msg):
            result = NetCDFTimeConverter().convert(val, None, None)


if __name__ == "__main__":
    unittest.main()
