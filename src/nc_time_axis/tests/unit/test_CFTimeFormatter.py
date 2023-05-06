"""Unit tests for the `nc_time_axis.CFTimeFormatter` class."""
import pytest

from nc_time_axis import CFTimeFormatter

FORMATS = {
    "%H:%M:%S": "01:01:01",
    "%H:%M": "01:01",
    "%Y-%m-%d %H:%M": "2000-01-01 01:01",
    "%Y-%m-%d": "2000-01-01",
    "%Y-%m": "2000-01",
    "%Y": "2000",
}


@pytest.mark.parametrize(("format", "expected"), FORMATS.items())
def test_CFTimeFormatter(format, expected):
    days = 3661 / 86400
    calendar = "360_day"
    formatter = CFTimeFormatter(format, calendar)
    result = formatter(days)
    assert result == expected
