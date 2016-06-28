"""Unit tests for the `nc-time-axis.NetCDFTimeDateFormatter` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

import unittest

import mock

from nc_time_axis import NetCDFTimeDateFormatter


class Test_pick_format(unittest.TestCase):
    def check(self, ndays):
        locator = mock.MagicMock()
        formatter = NetCDFTimeDateFormatter(locator, '360_day',
                                            'days since 2000-01-01 00:00')
        return formatter.pick_format(ndays)

    def test(self):
        self.assertEqual(self.check(0.1), '%H:%M:%S')
        self.assertEqual(self.check(0.6), '%H:%M')
        self.assertEqual(self.check(5), '%Y-%m-%d %H:%M')
        self.assertEqual(self.check(40), '%Y-%m-%d')
        self.assertEqual(self.check(300), '%Y-%m')
        self.assertEqual(self.check(1000), '%Y')


if __name__ == "__main__":
    unittest.main()
