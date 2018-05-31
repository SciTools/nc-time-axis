"""Unit tests for the `nc-time-axis.NetCDFTimeDateLocator` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import matplotlib.style
import matplotlib.dates as mdates
import cftime
import numpy as np

from nc_time_axis import NetCDFTimeDateLocator


matplotlib.style.use('classic')


class Test_compute_resolution(unittest.TestCase):
    def setUp(self):
        self.date_unit = 'days since 2004-01-01 00:00'
        self.calendar = '365_day'

    def check(self, max_n_ticks, num1, num2):
        locator = NetCDFTimeDateLocator(max_n_ticks=max_n_ticks,
                                        calendar=self.calendar,
                                        date_unit=self.date_unit)
        utime = cftime.utime(self.date_unit, self.calendar)
        return locator.compute_resolution(num1, num2, utime.num2date(num1),
                                          utime.num2date(num2))

    def test_one_minute(self):
        self.assertEqual(self.check(20, 0, 0.0003),
                         ('SECONDLY', mdates.SEC_PER_DAY))
        self.assertEqual(self.check(10, 0.0003, 0),
                         ('SECONDLY', mdates.SEC_PER_DAY))

    def test_one_hour(self):
        self.assertEqual(self.check(1, 0, 0.02), ('MINUTELY', 0))
        self.assertEqual(self.check(0.02*86400, 0, 0.02),
                         ('SECONDLY', mdates.SEC_PER_DAY))

    def test_one_day(self):
        self.assertEqual(self.check(1, 0, 1), ('HOURLY', 0))
        self.assertEqual(self.check(24, 0, 1), ('MINUTELY', 0))
        self.assertEqual(self.check(86400, 0, 1),
                         ('SECONDLY', mdates.SEC_PER_DAY))

    def test_30_days(self):
        self.assertEqual(self.check(1, 0, 30), ('DAILY', 30))
        self.assertEqual(self.check(30, 0, 30), ('HOURLY', 1))
        self.assertEqual(self.check(30*24, 0, 30),
                         ('MINUTELY', 0))
        self.assertEqual(self.check(30*86400, 0, 30),
                         ('SECONDLY', mdates.SEC_PER_DAY))

    def test_365_days(self):
        self.assertEqual(self.check(1, 0, 365), ('MONTHLY', 12))
        self.assertEqual(self.check(13, 0, 365), ('DAILY', 365))
        self.assertEqual(self.check(365, 0, 365), ('HOURLY', 15))
        self.assertEqual(self.check(365*24, 0, 365),
                         ('MINUTELY', 0))
        self.assertEqual(self.check(365*86400, 0, 365),
                         ('SECONDLY', mdates.SEC_PER_DAY))

    def test_10_years(self):
        self.assertEqual(self.check(1, 0, 10*365),
                         ('YEARLY', 10))
        self.assertEqual(self.check(10, 0, 10*365),
                         ('MONTHLY', 121))
        self.assertEqual(self.check(122, 0, 10*365),
                         ('DAILY', 10*365))
        self.assertEqual(self.check(10*365, 0, 10*365),
                         ('HOURLY', 152))
        self.assertEqual(self.check(10*365*24, 0, 10*365),
                         ('MINUTELY', 2))
        self.assertEqual(self.check(10*365*86400, 0, 10*365),
                         ('SECONDLY', mdates.SEC_PER_DAY))


class Test_tick_values(unittest.TestCase):
    def setUp(self):
        self.date_unit = 'days since 2004-01-01 00:00'
        self.calendar = '365_day'

    def check(self, max_n_ticks, num1, num2):
        locator = NetCDFTimeDateLocator(max_n_ticks=max_n_ticks,
                                        calendar=self.calendar,
                                        date_unit=self.date_unit)
        return locator.tick_values(num1, num2)

    def test_secondly(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 0, 0.0004),
            [0., 0.000116, 0.000231, 0.000347, 0.000463])

    def test_minutely(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 1, 1.07), [1., 1.027778, 1.055556, 1.083333])

    def test_hourly(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 2, 3), [2., 2.333333, 2.666667, 3.])

    def test_daily(self):
        np.testing.assert_array_equal(
            self.check(5, 0, 30), [0., 7., 14., 21., 28., 35.])

    def test_monthly(self):
        np.testing.assert_array_equal(
            self.check(4, 0, 365), [31., 120., 212., 304., 396.])

    def test_yearly(self):
        np.testing.assert_array_equal(
            self.check(5, 0, 5*365), [31., 485., 942., 1399., 1856.])


if __name__ == "__main__":
    unittest.main()
