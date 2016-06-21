"""Unit tests for the `nc-time-axis.NetCDFTimeConverter` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import netcdftime
import numpy as np

from nc_time_axis import NetCDFTimeConverter


class Test_axisinfo(unittest.TestCase):
    def test_default_limits(self):
        unit = ('360_day', 'days since 2000-02-25 00:00:00')
        result = NetCDFTimeConverter().axisinfo(unit, None)
        np.testing.assert_array_equal(result.default_limits,
                                      [netcdftime.datetime(2000, 1, 1),
                                       netcdftime.datetime(2010, 1, 1)])


class Test_default_units(unittest.TestCase):
    def test_360_day_calendar(self):
        calendar = '360_day'
        unit = 'days since 2000-01-01'
        val = [netcdftime.datetime(2014, 8, 12)]
        val[0].calendar = calendar
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit))

    def test_no_calendar_attribute(self):
        val = [netcdftime.datetime(2014, 8, 12)]
        msg = 'Expecting netcdftimes with an extra "calendar" attribute.'
        with self.assertRaisesRegexp(ValueError, msg):
            result = NetCDFTimeConverter().default_units(val, None)


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
        val = netcdftime.datetime(2014, 8, 12)
        val.calendar = '365_day'
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, 5333.)

    def test_netcdftime_np_array(self):
        val = np.array([netcdftime.datetime(2012, 6, 4)], dtype=np.object)
        for date in val:
            date.calendar = '360_day'
        result = NetCDFTimeConverter().convert(val, None, None)
        self.assertEqual(result, np.array([4473.]))

    def test_no_calendar_attribute(self):
        val = netcdftime.datetime(2014, 8, 12)
        msg = 'A "calendar" attribute must be attached'
        with self.assertRaisesRegexp(ValueError, msg):
            result = NetCDFTimeConverter().convert(val, None, None)


if __name__ == "__main__":
    unittest.main()
