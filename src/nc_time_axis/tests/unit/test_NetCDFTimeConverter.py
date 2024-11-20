"""Unit tests for the `nc-time-axis.NetCDFTimeConverter` class."""

import unittest

import cftime
import numpy as np
import pytest

from nc_time_axis import CalendarDateTime, NetCDFTimeConverter


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
class Test_axisinfo(unittest.TestCase):
    def test_axis_default_limits(self):
        cal = "360_day"
        unit = (cal, "days since 2000-02-25 00:00:00", CalendarDateTime)
        result = NetCDFTimeConverter().axisinfo(unit, None)
        expected_dt = [
            cftime.datetime(2000, 1, 1),
            cftime.datetime(2010, 1, 1),
        ]
        np.testing.assert_array_equal(
            result.default_limits,
            [CalendarDateTime(edt, cal) for edt in expected_dt],
        )


class Test_default_units(unittest.TestCase):
    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_360_day_calendar_point_CalendarDateTime(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = CalendarDateTime(cftime.datetime(2014, 8, 12), calendar)
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, CalendarDateTime))

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_360_day_calendar_list_CalendarDateTime(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = [CalendarDateTime(cftime.datetime(2014, 8, 12), calendar)]
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, CalendarDateTime))

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_360_day_calendar_nd_CalendarDateTime(self):
        # Test the case where the input is an nd-array.
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = np.array(
            [
                [CalendarDateTime(cftime.datetime(2014, 8, 12), calendar)],
                [CalendarDateTime(cftime.datetime(2014, 8, 13), calendar)],
            ]
        )
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, CalendarDateTime))

    def test_360_day_calendar_point_raw_date(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = cftime.Datetime360Day(2014, 8, 12)
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.Datetime360Day))

    def test_360_day_calendar_list_raw_date(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = [cftime.Datetime360Day(2014, 8, 12)]
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.Datetime360Day))

    def test_360_day_calendar_nd_raw_date(self):
        # Test the case where the input is an nd-array.
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = np.array(
            [
                [cftime.Datetime360Day(2014, 8, 12)],
                [cftime.Datetime360Day(2014, 8, 13)],
            ]
        )
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.Datetime360Day))

    def test_360_day_calendar_point_raw_universal_date(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = cftime.datetime(2014, 8, 12, calendar=calendar)
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.datetime))

    def test_360_day_calendar_list_raw_universal_date(self):
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = [cftime.datetime(2014, 8, 12, calendar=calendar)]
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.datetime))

    def test_360_day_calendar_nd_raw_universal_date(self):
        # Test the case where the input is an nd-array.
        calendar = "360_day"
        unit = "days since 2000-01-01"
        val = np.array(
            [
                [cftime.datetime(2014, 8, 12, calendar=calendar)],
                [cftime.datetime(2014, 8, 13, calendar=calendar)],
            ]
        )
        result = NetCDFTimeConverter().default_units(val, None)
        self.assertEqual(result, (calendar, unit, cftime.datetime))

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_nonequal_calendars(self):
        # Test that different supplied calendars causes an error.
        calendar_1 = "360_day"
        calendar_2 = "365_day"
        val = [
            CalendarDateTime(cftime.datetime(2014, 8, 12), calendar_1),
            CalendarDateTime(cftime.datetime(2014, 8, 13), calendar_2),
        ]
        with self.assertRaisesRegex(ValueError, "not all equal"):
            NetCDFTimeConverter().default_units(val, None)

    def test_no_calendar_point_raw_universal_date(self):
        calendar = None
        val = cftime.datetime(2014, 8, 12, calendar=calendar)
        with self.assertRaisesRegex(ValueError, "defined"):
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
        # TODO: remove this test once the minimum version of matplotlib
        # supported is at least 3.5.  See GitHub issue 97 for more details.
        val = 4
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    def test_numeric_iterable(self):
        # TODO: remove this test once the minimum version of matplotlib
        # supported is at least 3.5.  See GitHub issue 97 for more details.
        val = [12, 18]
        result = NetCDFTimeConverter().convert(val, None, None)
        np.testing.assert_array_equal(result, val)

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_cftime_CalendarDateTime(self):
        val = CalendarDateTime(cftime.datetime(2014, 8, 12), "365_day")
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert np.isscalar(result)

    def test_cftime_raw_date(self):
        val = cftime.DatetimeNoLeap(2014, 8, 12)
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert np.isscalar(result)

    def test_cftime_list_date(self):
        val = [cftime.DatetimeNoLeap(2014, 8, 12)]
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert len(result) == 1

    def test_cftime_tuple_date(self):
        val = (cftime.DatetimeNoLeap(2014, 8, 12),)
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert len(result) == 1

    def test_cftime_raw_universal_date(self):
        val = cftime.datetime(2014, 8, 12, calendar="noleap")
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert np.isscalar(result)

    def test_cftime_list_universal_date(self):
        val = [cftime.datetime(2014, 8, 12, calendar="noleap")]
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert len(result) == 1

    def test_cftime_tuple_univeral_date(self):
        val = (cftime.datetime(2014, 8, 12, calendar="noleap"),)
        result = NetCDFTimeConverter().convert(val, None, None)
        expected = 5333.0
        assert result == expected
        assert len(result) == 1

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_cftime_np_array_CalendarDateTime(self):
        val = np.array(
            [CalendarDateTime(cftime.datetime(2012, 6, 4), "360_day")],
            dtype=object,
        )
        result = NetCDFTimeConverter().convert(val, None, None)
        self.assertEqual(result, np.array([4473.0]))

    def test_cftime_np_array_raw_date(self):
        val = np.array([cftime.Datetime360Day(2012, 6, 4)], dtype=object)
        result = NetCDFTimeConverter().convert(val, None, None)
        self.assertEqual(result, np.array([4473.0]))

    def test_cftime_np_array_raw_universal_date(self):
        val = np.array([cftime.datetime(2012, 6, 4, calendar="360_day")], dtype=object)
        result = NetCDFTimeConverter().convert(val, None, None)
        self.assertEqual(result, np.array([4473.0]))

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_non_cftime_datetime(self):
        val = CalendarDateTime(4, "360_day")
        msg = (
            "The datetime attribute of the CalendarDateTime object must "
            "be of type `cftime.datetime`."
        )
        with self.assertRaisesRegex(ValueError, msg):
            _ = NetCDFTimeConverter().convert(val, None, None)

    def test_non_CalendarDateTime(self):
        val = "test"
        msg = (
            "The values must be numbers or instances of "
            '"nc_time_axis.CalendarDateTime".'
        )
        with self.assertRaisesRegex(ValueError, msg):
            _ = NetCDFTimeConverter().convert(val, None, None)


if __name__ == "__main__":
    unittest.main()
