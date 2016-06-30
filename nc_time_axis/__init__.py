"""
Support for netcdftime axis in matplotlib.

"""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

from collections import namedtuple
import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.units as munits
import netcdftime
import numpy as np

# Define __version__ based on versioneer's interpretation.
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


# Lower and upper are in number of days.
FormatOption = namedtuple('FormatOption', ['lower', 'upper', 'format_string'])


class CalendarDateTime(object):
    """
    Container for :class:`netcdftime.datetime` object and calendar.

    """
    def __init__(self, datetime, calendar):
        self.datetime = datetime
        self.calendar = calendar

    def __repr__(self):
        msg = '<{}: datetime={}, calendar={}>'
        return msg.format(type(self).__name__, self.datetime, self.calendar)


class NetCDFTimeDateFormatter(mticker.Formatter):
    """
    Formatter for netcdftime.datetime data.

    """
    # Some magic numbers. These seem to work pretty well.
    format_options = [FormatOption(0.0, 0.2, '%H:%M:%S'),
                      FormatOption(0.2, 0.8, '%H:%M'),
                      FormatOption(0.8, 15, '%Y-%m-%d %H:%M'),
                      FormatOption(15, 90, '%Y-%m-%d'),
                      FormatOption(90, 900, '%Y-%m'),
                      FormatOption(900, 6000000, '%Y')]

    def __init__(self, locator, calendar, time_units):
        #: The locator associated with this formatter. This is used to get hold
        #: of the scaling information.
        self.locator = locator
        self.calendar = calendar
        self.time_units = time_units

    def pick_format(self, ndays):
        """
        Returns a format string for an interval of the given number of days.

        """
        for option in self.format_options:
            if option.lower < ndays <= option.upper:
                return option.format_string
        else:
            msg = 'No formatter found for an interval of {} days.'
            raise ValueError(msg.format(ndays))

    def __call__(self, x, pos=0):
        format_string = self.pick_format(ndays=self.locator.ndays)
        dt = netcdftime.utime(self.time_units, self.calendar).num2date(x)
        return dt.strftime(format_string)


class NetCDFTimeDateLocator(mticker.Locator):
    """
    Determines tick locations when plotting netcdftime.datetime data.

    """
    def __init__(self, max_n_ticks, calendar, date_unit, min_n_ticks=3):
        # The date unit must be in the form of days since ...

        self.max_n_ticks = max_n_ticks
        self.min_n_ticks = min_n_ticks
        self._max_n_locator = mticker.MaxNLocator(max_n_ticks, integer=False)
        self._max_n_locator_days = mticker.MaxNLocator(
            max_n_ticks, integer=False, steps=[1, 2, 4, 7, 14])
        self.calendar = calendar
        self.date_unit = date_unit
        if not self.date_unit.lower().startswith('days since'):
            msg = 'The date unit must be days since for a NetCDF time locator.'
            raise ValueError(msg)

        self._cached_resolution = {}

    def compute_resolution(self, num1, num2, date1, date2):
        """
        Returns the resolution of the dates (hourly, minutely, yearly), and
        an **approximate** number of those units.

        """
        num_days = float(np.abs(num1 - num2))
        resolution = 'SECONDLY'
        n = mdates.SEC_PER_DAY
        if num_days * mdates.MINUTES_PER_DAY > self.max_n_ticks:
            resolution = 'MINUTELY'
            n = int(num_days / mdates.MINUTES_PER_DAY)
        if num_days * mdates.HOURS_PER_DAY > self.max_n_ticks:
            resolution = 'HOURLY'
            n = int(num_days / mdates.HOURS_PER_DAY)
        if num_days > self.max_n_ticks:
            resolution = 'DAILY'
            n = int(num_days)
        if num_days > 30 * self.max_n_ticks:
            resolution = 'MONTHLY'
            n = num_days // 30
        if num_days > 365 * self.max_n_ticks:
            resolution = 'YEARLY'
            n = abs(date1.year - date2.year)

        return resolution, n

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        vmin, vmax = mtransforms.nonsingular(vmin, vmax, expander=1e-7,
                                             tiny=1e-13)

        self.ndays = float(abs(vmax - vmin))

        utime = netcdftime.utime(self.date_unit, self.calendar)
        lower = utime.num2date(vmin)
        upper = utime.num2date(vmax)

        resolution, n = self.compute_resolution(vmin, vmax, lower, upper)

        if resolution == 'YEARLY':
            # TODO START AT THE BEGINNING OF A DECADE/CENTURY/MILLENIUM as
            # appropriate.
            years = self._max_n_locator.tick_values(lower.year, upper.year)
            ticks = [netcdftime.datetime(int(year), 1, 1) for year in years]
        elif resolution == 'MONTHLY':
            # TODO START AT THE BEGINNING OF A DECADE/CENTURY/MILLENIUM as
            # appropriate.
            months_offset = self._max_n_locator.tick_values(0, n)
            ticks = []
            for offset in months_offset:
                year = lower.year + np.floor((lower.month + offset) / 12)
                month = ((lower.month + offset) % 12) + 1
                ticks.append(netcdftime.datetime(int(year), int(month), 1))
        elif resolution == 'DAILY':
            # TODO: It would be great if this favoured multiples of 7.
            days = self._max_n_locator_days.tick_values(vmin, vmax)
            ticks = [utime.num2date(dt) for dt in days]
        elif resolution == 'HOURLY':
            hour_unit = 'hours since 2000-01-01'
            in_hours = utime.date2num([lower, upper])
            hours = self._max_n_locator.tick_values(in_hours[0], in_hours[1])
            ticks = [utime.num2date(dt) for dt in hours]
        elif resolution == 'MINUTELY':
            minute_unit = 'minutes since 2000-01-01'
            in_minutes = utime.date2num([lower, upper])
            minutes = self._max_n_locator.tick_values(in_minutes[0],
                                                      in_minutes[1])
            ticks = [utime.num2date(dt) for dt in minutes]
        elif resolution == 'SECONDLY':
            second_unit = 'seconds since 2000-01-01'
            in_seconds = utime.date2num([lower, upper])
            seconds = self._max_n_locator.tick_values(in_seconds[0],
                                                      in_seconds[1])
            ticks = [utime.num2date(dt) for dt in seconds]
        else:
            msg = 'Resolution {} not implemented yet.'.format(resolution)
            raise ValueError(msg)

        return utime.date2num(ticks)


class NetCDFTimeConverter(mdates.DateConverter):
    """
    Converter for netcdftime.datetime data.

    """
    standard_unit = 'days since 2000-01-01'

    @staticmethod
    def axisinfo(unit, axis):
        """
        Returns the :class:`~matplotlib.units.AxisInfo` for *unit*.

        *unit* is a tzinfo instance or None.
        The *axis* argument is required but not used.
        """
        calendar, date_unit = unit

        majloc = NetCDFTimeDateLocator(4, calendar=calendar,
                                       date_unit=date_unit)
        majfmt = NetCDFTimeDateFormatter(majloc, calendar=calendar,
                                         time_units=date_unit)
        datemin = CalendarDateTime(netcdftime.datetime(2000, 1, 1), calendar)
        datemax = CalendarDateTime(netcdftime.datetime(2010, 1, 1), calendar)
        return munits.AxisInfo(majloc=majloc, majfmt=majfmt, label='',
                               default_limits=(datemin, datemax))

    @classmethod
    def default_units(cls, sample_point, axis):
        """
        Computes some units for the given data point.

        """
        try:
            # Try getting the first item. Otherwise we just use this item.
            sample_point = sample_point[0]
        except (TypeError, IndexError):
            pass

        if not hasattr(sample_point, 'calendar'):
            msg = 'Expecting netcdftimes with an extra "calendar" attribute.'
            raise ValueError(msg)

        return sample_point.calendar, cls.standard_unit

    @classmethod
    def convert(cls, value, unit, axis):
        """
        Converts value, if it is not already a number or sequence of numbers,
        with :func:`netcdftime.utime().date2num`.

        """
        if isinstance(value, np.ndarray):
            # Don't do anything with numeric types.
            if value.dtype != np.object:
                return value

            first_value = value[0]
        else:
            # Don't do anything with numeric types.
            if munits.ConversionInterface.is_numlike(value):
                return value
            first_value = value

        if not isinstance(first_value, CalendarDateTime):
            raise ValueError('The values must be numbers or instances of '
                             '"nc_time_axis.CalendarDateTime".')

        if not isinstance(first_value.datetime, netcdftime.datetime):
            raise ValueError('The datetime attribute of the CalendarDateTime '
                             'object must be of type `netcdftime.datetime`.')

        ut = netcdftime.utime(cls.standard_unit, calendar=first_value.calendar)

        if isinstance(value, CalendarDateTime):
            value = [value]

        return ut.date2num([v.datetime for v in value])


# Automatically register NetCDFTimeConverter with matplotlib.unit's converter
# dictionary.
if CalendarDateTime not in munits.registry:
    munits.registry[CalendarDateTime] = NetCDFTimeConverter()
