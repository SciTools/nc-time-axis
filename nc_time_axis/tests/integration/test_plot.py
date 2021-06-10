"""Integration test for plotting data with non-gregorian calendar."""

import unittest

import matplotlib

matplotlib.use("agg")
import cftime
import matplotlib.pyplot as plt
import numpy as np

import nc_time_axis


class Test(unittest.TestCase):
    def setUp(self):
        # Make sure we have no unclosed plots from previous tests before
        # generating this one.
        plt.close("all")

    def tearDown(self):
        # If a plotting test bombs out it can leave the current figure
        # in an odd state, so we make sure it's been disposed of.
        plt.close("all")

    def test_360_day_calendar_CalendarDateTime(self):
        calendar = "360_day"
        datetimes = [
            cftime.datetime(1986, month, 30, calendar=calendar)
            for month in range(1, 6)
        ]
        cal_datetimes = [
            nc_time_axis.CalendarDateTime(dt, calendar) for dt in datetimes
        ]
        (line1,) = plt.plot(cal_datetimes)
        result_ydata = line1.get_ydata()
        np.testing.assert_array_equal(result_ydata, cal_datetimes)

    def test_360_day_calendar_raw_dates(self):
        datetimes = [
            cftime.Datetime360Day(1986, month, 30) for month in range(1, 6)
        ]
        (line1,) = plt.plot(datetimes)
        result_ydata = line1.get_ydata()
        np.testing.assert_array_equal(result_ydata, datetimes)


if __name__ == "__main__":
    unittest.main()
