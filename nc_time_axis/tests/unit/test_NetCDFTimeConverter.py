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
            result.default_limits,
            [CalendarDateTime(edt, cal) for edt in expected_dt])


class Test_default_units(unittest.TestCase):
    def test_360_day_calendar_point(self):
        calendar = '360_day'
        unit = 'days since 2000-01-01'
        val = CalendarDateTime(netcdftime.datetime(2014, 8, 12), calendar)
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit))

    def test_360_day_calendar_list(self):
        calendar = '360_day'
        unit = 'days since 2000-01-01'
        val = [CalendarDateTime(netcdftime.datetime(2014, 8, 12), calendar)]
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit))

    def test_360_day_calendar_nd(self):
        # Test the case where the input is an nd-array.
        calendar = '360_day'
        unit = 'days since 2000-01-01'
        val = np.array([[CalendarDateTime(netcdftime.datetime(2014, 8, 12),
                                          calendar)],
                       [CalendarDateTime(netcdftime.datetime(2014, 8, 13),
                                         calendar)]])
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit))

    def test_nonequal_calendars(self):
        # Test that different supplied calendars causes an error.
        calendar_1 = '360_day'
        calendar_2 = '365_day'
        unit = 'days since 2000-01-01'
        val = [CalendarDateTime(netcdftime.datetime(2014, 8, 12), calendar_1),
               CalendarDateTime(netcdftime.datetime(2014, 8, 13), calendar_2)]
        with self.assertRaisesRegexp(ValueError, 'not all equal'):
            NetCDFTimeConverter().default_units(val, None)


class Test_convert(unittest.TestCase):
    def test_numpy_array(self):
        val = np.array([7])
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    def test_numpy_nd_array(self):
        shape = (4, 2)
        val = np.arange(8).reshape(shape)
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)
        self.assertEqual(result.shape, shape)

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

    def test_non_CalendarDateTime(self):
        val = netcdftime.datetime(1988, 5, 6)
        msg = 'The values must be numbers or instances of ' \
              '"nc_time_axis.CalendarDateTime".'
        with self.assertRaisesRegexp(ValueError, msg):
            result = NetCDFTimeConverter().convert(val, None, None)


if __name__ == "__main__":
    unittest.main()
