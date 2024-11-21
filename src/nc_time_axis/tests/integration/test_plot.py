"""Integration test for plotting data with non-gregorian calendar."""

import unittest
import warnings

import matplotlib

matplotlib.use("agg")
import cftime
import matplotlib.pyplot as plt
import numpy as np
import pytest

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

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_360_day_calendar_CalendarDateTime(self):
        calendar = "360_day"
        datetimes = [
            cftime.datetime(1986, month, 30, calendar=calendar) for month in range(1, 6)
        ]
        cal_datetimes = [
            nc_time_axis.CalendarDateTime(dt, calendar) for dt in datetimes
        ]
        (line1,) = plt.plot(cal_datetimes)
        result_ydata = line1.get_ydata()
        np.testing.assert_array_equal(result_ydata, cal_datetimes)

    def test_360_day_calendar_raw_dates(self):
        datetimes = [cftime.Datetime360Day(1986, month, 30) for month in range(1, 6)]
        (line1,) = plt.plot(datetimes)
        result_ydata = line1.get_ydata()
        np.testing.assert_array_equal(result_ydata, datetimes)

    def test_360_day_calendar_raw_universal_dates(self):
        datetimes = [
            cftime.datetime(1986, month, 30, calendar="360_day")
            for month in range(1, 6)
        ]
        (line1,) = plt.plot(datetimes)
        result_ydata = line1.get_ydata()
        np.testing.assert_array_equal(result_ydata, datetimes)

    def test_no_calendar_raw_universal_dates(self):
        datetimes = [
            cftime.datetime(1986, month, 30, calendar=None) for month in range(1, 6)
        ]
        with self.assertRaisesRegex(ValueError, "defined"):
            plt.plot(datetimes)

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_fill_between(self):
        calendar = "360_day"
        dt = [
            cftime.datetime(year=2017, month=2, day=day, calendar=calendar)
            for day in range(1, 31)
        ]
        cdt = [nc_time_axis.CalendarDateTime(item, calendar) for item in dt]
        temperatures = [np.round(np.random.uniform(0, 12), 3) for _ in range(len(cdt))]

        plt.fill_between(cdt, temperatures, 0)


def setup_function(function):
    plt.close()


def teardown_function(function):
    plt.close()


with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    TICKS = {
        "List[cftime.datetime]": [cftime.Datetime360Day(1986, 2, 1)],
        "List[CalendarDateTime]": [
            nc_time_axis.CalendarDateTime(cftime.Datetime360Day(1986, 2, 1), "360_day")
        ],
    }


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize("axis", ["x", "y"])
@pytest.mark.parametrize("ticks", TICKS.values(), ids=list(TICKS.keys()))
def test_set_ticks(axis, ticks):
    times = [cftime.Datetime360Day(1986, month, 30) for month in range(1, 6)]
    data = range(len(times))
    fig, ax = plt.subplots(1, 1)
    if axis == "x":
        ax.plot(times, data)
        ax.set_xticks(ticks)
        fig.canvas.draw()
        ticklabels = ax.get_xticklabels()
    else:
        ax.plot(data, times)
        ax.set_yticks(ticks)
        fig.canvas.draw()
        ticklabels = ax.get_yticklabels()
    result_labels = [label.get_text() for label in ticklabels]
    expected_labels = ["1986-02-01"]
    assert result_labels == expected_labels


@pytest.mark.parametrize("axis", ["x", "y"])
@pytest.mark.parametrize("ticks", TICKS.values(), ids=list(TICKS.keys()))
def test_set_ticks_with_CFTimeFormatter(axis, ticks):
    times = [cftime.Datetime360Day(1986, month, 30) for month in range(1, 6)]
    data = range(len(times))
    fig, ax = plt.subplots(1, 1)
    formatter = nc_time_axis.CFTimeFormatter("%Y-%m", "360_day")
    if axis == "x":
        ax.plot(times, data)
        ax.set_xticks(ticks)
        ax.xaxis.set_major_formatter(formatter)
        fig.canvas.draw()
        ticklabels = ax.get_xticklabels()
    else:
        ax.plot(data, times)
        ax.set_yticks(ticks)
        ax.yaxis.set_major_formatter(formatter)
        fig.canvas.draw()
        ticklabels = ax.get_yticklabels()
    result_labels = [label.get_text() for label in ticklabels]
    expected_labels = ["1986-02"]
    assert result_labels == expected_labels


@pytest.mark.parametrize("axis", ["x", "y"])
def test_set_format_with_CFTimeFormatter_with_default_ticks(axis):
    times = [cftime.Datetime360Day(1986, month, 30) for month in range(1, 6)]
    data = range(len(times))
    fig, ax = plt.subplots(1, 1)
    formatter = nc_time_axis.CFTimeFormatter("%Y", "360_day")
    if axis == "x":
        ax.plot(times, data)
        ax.xaxis.set_major_formatter(formatter)
        fig.canvas.draw()
        ticklabels = ax.get_xticklabels()
    else:
        ax.plot(data, times)
        ax.yaxis.set_major_formatter(formatter)
        fig.canvas.draw()
        ticklabels = ax.get_yticklabels()
    result_labels = [label.get_text() for label in ticklabels]
    expected_labels = ["1986", "1986", "1986", "1986", "1986"]
    assert result_labels == expected_labels


if __name__ == "__main__":
    unittest.main()
