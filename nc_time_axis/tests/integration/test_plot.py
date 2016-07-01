"""Integration test for plotting data with non-gregorian calendar."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  # nopep8
import netcdftime  # nopep8
import numpy as np  # nopep8

import nc_time_axis  # nopep8


class Test(unittest.TestCase):
    def setUp(self):
        # Make sure we have no unclosed plots from previous tests before
        # generating this one.
        plt.close('all')

    def tearDown(self):
        # If a plotting test bombs out it can leave the current figure
        # in an odd state, so we make sure it's been disposed of.
        plt.close('all')

    def test_360_day_calendar(self):
        datetimes = [netcdftime.datetime(1986, month, 30)
                     for month in range(1, 6)]
        cal_datetimes = [nc_time_axis.CalendarDateTime(dt, '360_day')
                         for dt in datetimes]
        line1, = plt.plot(cal_datetimes)
        result_ydata = line1.get_ydata()
        result_datetimes = [cdt.datetime for cdt in result_ydata]
        np.testing.assert_array_equal(result_datetimes, datetimes)
        self.assertIs('360_day', result_ydata[0].calendar)


if __name__ == "__main__":
    unittest.main()
