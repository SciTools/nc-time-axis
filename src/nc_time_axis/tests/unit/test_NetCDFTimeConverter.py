"""Unit tests for the `nc-time-axis.NetCDFTimeConverter` class."""

import re
import unittest

import cftime
import numpy as np
import pytest

from nc_time_axis import _CALENDARS, CalendarDateTime, NetCDFTimeConverter


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
        val = object
        msg = (
            "The values must be numbers or instances of "
            '"nc_time_axis.CalendarDateTime".'
        )
        with self.assertRaisesRegex(ValueError, msg):
            _ = NetCDFTimeConverter().convert(val, None, None)


DATETIME_STR_TEST_CASES = (
    ("2014", (2014, 1, 1)),
    ("2014-02", (2014, 2, 1)),
    ("2015-03-07", (2015, 3, 7)),
    ("2015-03-07 12", (2015, 3, 7, 12)),
    ("2015-03-07 12:11", (2015, 3, 7, 12, 11)),
    ("2015-03-07 12:11:05", (2015, 3, 7, 12, 11, 5)),
    ("2015-03-07 12:11:05.111", (2015, 3, 7, 12, 11, 5, 111000)),
    ("2015-03-07 12:11:05.111456", (2015, 3, 7, 12, 11, 5, 111456)),
    # # variants with T
    # # year-month-day is the same
    ("2015-03-07T12", (2015, 3, 7, 12)),
    ("2015-03-07T12:11", (2015, 3, 7, 12, 11)),
    ("2015-03-07T12:11:05", (2015, 3, 7, 12, 11, 5)),
    ("2015-03-07T12:11:05.111", (2015, 3, 7, 12, 11, 5, 111000)),
    ("2015-03-07T12:11:05.111456", (2015, 3, 7, 12, 11, 5, 111456)),
    # variants with T and no sep
    ("201402", (2014, 2, 1)),
    ("20150307", (2015, 3, 7)),
    ("20150307T12", (2015, 3, 7, 12)),
    ("20150307T1211", (2015, 3, 7, 12, 11)),
    ("20150307T121105", (2015, 3, 7, 12, 11, 5)),
    ("20150307T121105.111", (2015, 3, 7, 12, 11, 5, 111000)),
    ("20150307T121105.111456", (2015, 3, 7, 12, 11, 5, 111456)),
)


class Test_convert_str_value:

    def test_wrong_units(self):

        # NOTE: 'convert' is unlikely to be called manually
        # units must be a tuple with 3 elements the first of which is the calendar

        msg = "unit must have 3 elements to unpack and the first must be the calendar"

        with pytest.raises(ValueError, match=msg):
            NetCDFTimeConverter().convert("str", None, None)

        with pytest.raises(ValueError, match=msg):
            NetCDFTimeConverter().convert("str", "noleap", None)

        with pytest.raises(ValueError, match=msg):
            NetCDFTimeConverter().convert("str", ("noleap",), None)

        with pytest.raises(ValueError, match=msg):
            NetCDFTimeConverter().convert("str", (None, None, None, None), None)

    def test_wrong_calendar(self):

        msg = "calendar must be one of 'standard',.* got 'invalid'"
        with pytest.raises(ValueError, match=msg):
            NetCDFTimeConverter().convert("str", ("invalid", None, None), None)

    @pytest.mark.parametrize("value", ["a", "2014+1", "2014-13"])
    def test_wrong_datetime(self, value):

        msg = f"no ISO-8601 or cftime-string-like match for string: {value}"
        with pytest.raises(ValueError, match=re.escape(msg)):
            NetCDFTimeConverter().convert(value, ("standard", None, None), None)

    @pytest.mark.parametrize(("date_str", "date_tuple"), DATETIME_STR_TEST_CASES)
    def test_convert(self, date_str, date_tuple):

        # do not parametrize to avoid an explosion of the number of test cases
        for calendar in _CALENDARS:
            datetime = cftime.datetime(*date_tuple, calendar=calendar)

            expected = cftime.date2num(
                datetime, NetCDFTimeConverter.standard_unit, calendar
            )

            result = NetCDFTimeConverter().convert(
                date_str, (calendar, None, None), None
            )

            assert expected == result, calendar


if __name__ == "__main__":
    unittest.main()
