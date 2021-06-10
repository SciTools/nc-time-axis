"""Unit tests for the `nc-time-axis.NetCDFTimeDateLocator` class."""


import unittest

import cftime
import matplotlib.dates as mdates
import matplotlib.style
import numpy as np

from nc_time_axis import NetCDFTimeDateLocator

matplotlib.style.use("classic")


class Test_compute_resolution(unittest.TestCase):
    def setUp(self):
        self.date_unit = "days since 2004-01-01 00:00"
        self.calendar = "365_day"

    def check(self, max_n_ticks, num1, num2):
        locator = NetCDFTimeDateLocator(
            max_n_ticks=max_n_ticks,
            calendar=self.calendar,
            date_unit=self.date_unit,
        )
        return locator.compute_resolution(
            num1,
            num2,
            cftime.num2date(num1, self.date_unit, calendar=self.calendar),
            cftime.num2date(num2, self.date_unit, calendar=self.calendar),
        )

    def test_one_minute(self):
        self.assertEqual(
            self.check(20, 0, 0.0003), ("SECONDLY", mdates.SEC_PER_DAY)
        )
        self.assertEqual(
            self.check(10, 0.0003, 0), ("SECONDLY", mdates.SEC_PER_DAY)
        )

    def test_one_hour(self):
        self.assertEqual(self.check(1, 0, 0.02), ("MINUTELY", 0))
        self.assertEqual(
            self.check(0.02 * 86400, 0, 0.02), ("SECONDLY", mdates.SEC_PER_DAY)
        )

    def test_one_day(self):
        self.assertEqual(self.check(1, 0, 1), ("HOURLY", 0))
        self.assertEqual(self.check(24, 0, 1), ("MINUTELY", 0))
        self.assertEqual(
            self.check(86400, 0, 1), ("SECONDLY", mdates.SEC_PER_DAY)
        )

    def test_30_days(self):
        self.assertEqual(self.check(1, 0, 30), ("DAILY", 30))
        self.assertEqual(self.check(30, 0, 30), ("HOURLY", 1))
        self.assertEqual(self.check(30 * 24, 0, 30), ("MINUTELY", 0))
        self.assertEqual(
            self.check(30 * 86400, 0, 30), ("SECONDLY", mdates.SEC_PER_DAY)
        )

    def test_365_days(self):
        self.assertEqual(self.check(1, 0, 365), ("MONTHLY", 12))
        self.assertEqual(self.check(13, 0, 365), ("DAILY", 365))
        self.assertEqual(self.check(365, 0, 365), ("HOURLY", 15))
        self.assertEqual(self.check(365 * 24, 0, 365), ("MINUTELY", 0))
        self.assertEqual(
            self.check(365 * 86400, 0, 365), ("SECONDLY", mdates.SEC_PER_DAY)
        )

    def test_10_years(self):
        self.assertEqual(self.check(1, 0, 10 * 365), ("YEARLY", 10))
        self.assertEqual(self.check(10, 0, 10 * 365), ("MONTHLY", 121))
        self.assertEqual(self.check(122, 0, 10 * 365), ("DAILY", 10 * 365))
        self.assertEqual(self.check(10 * 365, 0, 10 * 365), ("HOURLY", 152))
        self.assertEqual(
            self.check(10 * 365 * 24, 0, 10 * 365), ("MINUTELY", 2)
        )
        self.assertEqual(
            self.check(10 * 365 * 86400, 0, 10 * 365),
            ("SECONDLY", mdates.SEC_PER_DAY),
        )


class Test_tick_values(unittest.TestCase):
    def setUp(self):
        self.date_unit = "days since 2004-01-01 00:00"
        self.calendar = "365_day"

    def check(self, max_n_ticks, num1, num2):
        locator = NetCDFTimeDateLocator(
            max_n_ticks=max_n_ticks,
            calendar=self.calendar,
            date_unit=self.date_unit,
        )
        return locator.tick_values(num1, num2)

    def test_secondly(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 0, 0.0004),
            [0.0, 0.000116, 0.000231, 0.000347, 0.000463],
        )

    def test_minutely(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 1, 1.07), [1.0, 1.027778, 1.055556, 1.083333]
        )

    def test_hourly(self):
        np.testing.assert_array_almost_equal(
            self.check(4, 2, 3), [2.0, 2.333333, 2.666667, 3.0]
        )

    def test_daily(self):
        np.testing.assert_array_equal(
            self.check(5, 0, 30), [0.0, 7.0, 14.0, 21.0, 28.0, 35.0]
        )

    def test_monthly(self):
        np.testing.assert_array_equal(
            self.check(4, 0, 365), [31.0, 120.0, 212.0, 304.0, 396.0]
        )

    def test_yearly(self):
        np.testing.assert_array_equal(
            self.check(5, 0, 5 * 365), [31.0, 485.0, 942.0, 1399.0, 1856.0]
        )


class Test_tick_values_yr0(unittest.TestCase):
    def setUp(self):
        self.date_unit = "days since 0001-01-01 00:00"
        self.all_calendars = [
            "standard",
            "gregorian",
            "proleptic_gregorian",
            "noleap",
            "365_day",
            "360_day",
            "julian",
            "all_leap",
            "366_day",
        ]
        self.yr0_remove_calendars = [
            "proleptic_gregorian",
            "gregorian",
            "julian",
            "standard",
        ]

    def check(self, max_n_ticks, num1, num2, calendar):
        locator = NetCDFTimeDateLocator(
            max_n_ticks=max_n_ticks,
            calendar=calendar,
            date_unit=self.date_unit,
        )
        return locator.tick_values(num1, num2)

    def test_yearly_yr0_remove(self):
        for calendar in self.all_calendars:
            # convert values to dates, check that none of them has year 0
            ticks = self.check(5, 0, 100 * 365, calendar)
            year_ticks = [
                cftime.num2date(t, self.date_unit, calendar=calendar).year
                for t in ticks
            ]
            if calendar in self.yr0_remove_calendars:
                self.assertNotIn(0, year_ticks)
            else:
                self.assertIn(0, year_ticks)


if __name__ == "__main__":
    unittest.main()
