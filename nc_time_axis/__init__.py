"""
Support for cftime axis in matplotlib.

"""

# nc-time-axis provides datetime locator and formatter objects which are
# analogous to matplotlib's, but are compatible with cftime.datetime objects
# rather than standard library datetimes or np.datetime64 values. Because of
# this correspondence, some code contained in nc-time-axis is adapted from or
# directly copied from matplotlib.  For reference, we include a copy of
# matplotlib's license here.

# License agreement for matplotlib versions 1.3.0 and later
# =========================================================

# 1. This LICENSE AGREEMENT is between the Matplotlib Development Team
# ("MDT"), and the Individual or Organization ("Licensee") accessing and
# otherwise using matplotlib software in source or binary form and its
# associated documentation.

# 2. Subject to the terms and conditions of this License Agreement, MDT
# hereby grants Licensee a nonexclusive, royalty-free, world-wide license
# to reproduce, analyze, test, perform and/or display publicly, prepare
# derivative works, distribute, and otherwise use matplotlib
# alone or in any derivative version, provided, however, that MDT's
# License Agreement and MDT's notice of copyright, i.e., "Copyright (c)
# 2012- Matplotlib Development Team; All Rights Reserved" are retained in
# matplotlib  alone or in any derivative version prepared by
# Licensee.

# 3. In the event Licensee prepares a derivative work that is based on or
# incorporates matplotlib or any part thereof, and wants to
# make the derivative work available to others as provided herein, then
# Licensee hereby agrees to include in any such work a brief summary of
# the changes made to matplotlib .

# 4. MDT is making matplotlib available to Licensee on an "AS
# IS" basis.  MDT MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
# IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, MDT MAKES NO AND
# DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
# FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF MATPLOTLIB
# WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

# 5. MDT SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF MATPLOTLIB
#  FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
# LOSS AS A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING
# MATPLOTLIB , OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF
# THE POSSIBILITY THEREOF.

# 6. This License Agreement will automatically terminate upon a material
# breach of its terms and conditions.

# 7. Nothing in this License Agreement shall be deemed to create any
# relationship of agency, partnership, or joint venture between MDT and
# Licensee.  This License Agreement does not grant permission to use MDT
# trademarks or trade name in a trademark sense to endorse or promote
# products or services of Licensee, or any third party.

# 8. By copying, installing or otherwise using matplotlib ,
# Licensee agrees to be bound by the terms and conditions of this License
# Agreement.

# License agreement for matplotlib versions prior to 1.3.0
# ========================================================

# 1. This LICENSE AGREEMENT is between John D. Hunter ("JDH"), and the
# Individual or Organization ("Licensee") accessing and otherwise using
# matplotlib software in source or binary form and its associated
# documentation.

# 2. Subject to the terms and conditions of this License Agreement, JDH
# hereby grants Licensee a nonexclusive, royalty-free, world-wide license
# to reproduce, analyze, test, perform and/or display publicly, prepare
# derivative works, distribute, and otherwise use matplotlib
# alone or in any derivative version, provided, however, that JDH's
# License Agreement and JDH's notice of copyright, i.e., "Copyright (c)
# 2002-2011 John D. Hunter; All Rights Reserved" are retained in
# matplotlib  alone or in any derivative version prepared by
# Licensee.

# 3. In the event Licensee prepares a derivative work that is based on or
# incorporates matplotlib  or any part thereof, and wants to
# make the derivative work available to others as provided herein, then
# Licensee hereby agrees to include in any such work a brief summary of
# the changes made to matplotlib.

# 4. JDH is making matplotlib  available to Licensee on an "AS
# IS" basis.  JDH MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
# IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, JDH MAKES NO AND
# DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
# FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF MATPLOTLIB
# WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

# 5. JDH SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF MATPLOTLIB
#  FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR
# LOSS AS A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING
# MATPLOTLIB , OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF
# THE POSSIBILITY THEREOF.

# 6. This License Agreement will automatically terminate upon a material
# breach of its terms and conditions.

# 7. Nothing in this License Agreement shall be deemed to create any
# relationship of agency, partnership, or joint venture between JDH and
# Licensee.  This License Agreement does not grant permission to use JDH
# trademarks or trade name in a trademark sense to endorse or promote
# products or services of Licensee, or any third party.

# 8. By copying, installing or otherwise using matplotlib,
# Licensee agrees to be bound by the terms and conditions of this License
# Agreement.

import warnings
from numbers import Number

import cftime
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import matplotlib.units as munits
import numpy as np
from numpy import ma

from ._version import version as __version__  # noqa: F401

_DEFAULT_RESOLUTION = "DAILY"
_TIME_UNITS = "days since 2000-01-01"


class CalendarDateTime:
    """
    Container for a :py:class:`cftime.datetime` object and calendar.

    Parameters
    ----------
    datetime : :py:class:`cftime.datetime`
        The datetime instance associated with this
        :py:class:`CalendarDateTime` object.
    calendar : str
        The calendar type of the datetime object, e.g. ``"noleap"``.  See
        :py:class:`cftime.datetime` documentation for a full list of valid
        calendar strings.

    Notes
    -----
    This class is no longer needed and will be deprecated in nc-time-axis
    version 1.5.
    """

    def __init__(self, datetime, calendar):
        warnings.warn(
            "CalendarDateTime is obsolete and will be deprecated in nc_time_axis "
            "version 1.5.  Please consider switching to plotting instances or "
            "subclasses of cftime.datetime directly.",
            DeprecationWarning,
        )
        self.datetime = datetime
        self.calendar = calendar

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.datetime == other.datetime
            and self.calendar == other.calendar
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return (
            f"<{type(self).__name__}: datetime={self.datetime}, "
            "calendar={self.calendar}>"
        )


_RESOLUTION_TO_FORMAT = {
    "SECONDLY": "%H:%M:%S",
    "MINUTELY": "%H:%M",
    "HOURLY": "%Y-%m-%d %H:%M",
    "DAILY": "%Y-%m-%d",
    "MONTHLY": "%Y-%m",
    "YEARLY": "%Y",
}


class AutoCFTimeFormatter(mticker.Formatter):
    """
    Automatic formatter for :py:class:`cftime.datetime` data.

    Automatically chooses a date format based on the resolution set by the
    :py:class:`NetCDFDateTimeLocator`.  If no resolution is set, a default
    format of ``"%Y-%m-%d"`` is used.

    Parameters
    ----------
    locator : NetCDFDateTimeLocator
        The locator to be associated with this formatter.
    calendar : str
        The calendar type of the axis, e.g. ``"noleap"``.  See the
        :py:class:`cftime.datetime` documentation for a full list of valid
        calendar strings.
    time_units : str, optional
        The time units the numeric tick values represent.  Note this will
        be deprecated in nc-time-axis version 1.5.
    """

    def __init__(self, locator, calendar, time_units=None):
        #: The locator associated with this formatter. This is used to get hold
        #: of the scaling information.
        self.locator = locator
        self.calendar = calendar
        if time_units is not None:
            warnings.warn(
                "The time_units argument will be removed in nc_time_axis "
                "version 1.5",
                DeprecationWarning,
            )
            self.time_units = time_units
        else:
            self.time_units = _TIME_UNITS

    def pick_format(self, resolution):
        return _RESOLUTION_TO_FORMAT[resolution]

    def __call__(self, x, pos=0):
        format_string = self.pick_format(self.locator.resolution)
        dt = cftime.num2date(x, self.time_units, calendar=self.calendar)
        return dt.strftime(format_string)


class NetCDFTimeDateFormatter(AutoCFTimeFormatter):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "NetCDFTimeDateFormatter will be named AutoCFTimeFormatter "
            "in nc_time_axis version 1.5",
            FutureWarning,
        )
        super(NetCDFTimeDateFormatter, self).__init__(*args, **kwargs)


class CFTimeFormatter(mticker.Formatter):
    """
    A formatter for explicitly setting the format of a
    :py:class:`cftime.datetime` axis.

    Parameters
    ----------
    format : str Format string that can be passed to cftime.datetime.strftime,
        e.g. ``"%Y-%m-%d"``.  See `the Python documentation
        <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_
        for acceptable format codes.
    calendar : str
        The calendar type of the axis, e.g. ``"noleap"``.  See the
        :py:class:`cftime.datetime` documentation for a full list of valid
        calendar strings.
    """

    def __init__(self, format, calendar):
        self.format = format
        self.calendar = calendar

    def __call__(self, x, pos=0):
        dt = cftime.num2date(x, _TIME_UNITS, calendar=self.calendar)
        return dt.strftime(self.format)


class NetCDFTimeDateLocator(mticker.Locator):
    """
    Determines tick locations when plotting :py:class:`cftime.datetime` data.

    Parameters
    ----------
    max_n_ticks : int
        The maximum number of ticks along the axis.  This is passed internally
        to a :py:class:`matplotlib.ticker.MaxNLocator` class.
    calendar : str
        The calendar type of the axis, e.g. ``"noleap"``.  See the
        :py:class:`cftime.datetime` documentation for a full list of valid
        calendar strings.
    date_unit : str
        The time units the numeric tick values represent.  Note this will
        be deprecated in nc-time-axis version 1.5.
    min_n_ticks : int, default 3
        The minimum number of ticks along the axis. Note this is currently
        not used.
    """

    real_world_calendars = (
        "gregorian",
        "julian",
        "proleptic_gregorian",
        "standard",
    )

    def __init__(self, max_n_ticks, calendar, date_unit=None, min_n_ticks=3):
        # The date unit must be in the form of days since ...

        self.max_n_ticks = max_n_ticks
        self.min_n_ticks = min_n_ticks
        self._max_n_locator = mticker.MaxNLocator(max_n_ticks, integer=True)
        self._max_n_locator_days = mticker.MaxNLocator(
            max_n_ticks, integer=True, steps=[1, 2, 4, 7, 10]
        )
        self.calendar = calendar
        if date_unit is not None:
            warnings.warn(
                "The date_unit argument will be removed in "
                "nc_time_axis version 1.5",
                DeprecationWarning,
            )
            self.date_unit = date_unit
        else:
            self.date_unit = _TIME_UNITS
        if not self.date_unit.lower().startswith("days since"):
            emsg = (
                "The date unit must be days since for a NetCDF "
                "time locator."
            )
            raise ValueError(emsg)
        self.resolution = _DEFAULT_RESOLUTION
        self._cached_resolution = {}

    def compute_resolution(self, num1, num2, date1, date2):
        """
        Returns the resolution of the dates (hourly, minutely, yearly), and
        an **approximate** number of those units.

        """
        num_days = float(np.abs(num1 - num2))
        resolution = "SECONDLY"
        n = mdates.SEC_PER_DAY
        if num_days * mdates.MINUTES_PER_DAY > self.max_n_ticks:
            resolution = "MINUTELY"
            n = int(num_days / mdates.MINUTES_PER_DAY)
        if num_days * mdates.HOURS_PER_DAY > self.max_n_ticks:
            resolution = "HOURLY"
            n = int(num_days / mdates.HOURS_PER_DAY)
        if num_days > self.max_n_ticks:
            resolution = "DAILY"
            n = int(num_days)
        if num_days > 30 * self.max_n_ticks:
            resolution = "MONTHLY"
            n = num_days // 30
        if num_days > 365 * self.max_n_ticks:
            resolution = "YEARLY"
            n = abs(date1.year - date2.year)
        self.resolution = resolution
        return resolution, n

    def __call__(self):
        vmin, vmax = self.axis.get_view_interval()
        return self.tick_values(vmin, vmax)

    def tick_values(self, vmin, vmax):
        vmin, vmax = mtransforms.nonsingular(
            vmin, vmax, expander=1e-7, tiny=1e-13
        )
        lower = cftime.num2date(vmin, self.date_unit, calendar=self.calendar)
        upper = cftime.num2date(vmax, self.date_unit, calendar=self.calendar)

        resolution, n = self.compute_resolution(vmin, vmax, lower, upper)

        def has_year_zero(year):
            result = dict()
            if self.calendar in self.real_world_calendars and not bool(year):
                result = dict(has_year_zero=True)
            return result

        if resolution == "YEARLY":
            # TODO START AT THE BEGINNING OF A DECADE/CENTURY/MILLENIUM as
            # appropriate.

            years = self._max_n_locator.tick_values(lower.year, upper.year)
            ticks = [
                cftime.datetime(
                    int(year),
                    1,
                    1,
                    calendar=self.calendar,
                    **has_year_zero(year),
                )
                for year in years
            ]
        elif resolution == "MONTHLY":
            # TODO START AT THE BEGINNING OF A DECADE/CENTURY/MILLENIUM as
            # appropriate.
            months_offset = self._max_n_locator.tick_values(0, n)
            ticks = []
            for offset in months_offset:
                year = lower.year + np.floor((lower.month + offset) / 12)
                month = ((lower.month + offset) % 12) + 1
                dt = cftime.datetime(
                    int(year),
                    int(month),
                    1,
                    calendar=self.calendar,
                    **has_year_zero(year),
                )
                ticks.append(dt)
        elif resolution == "DAILY":
            # TODO: It would be great if this favoured multiples of 7.
            days = self._max_n_locator_days.tick_values(vmin, vmax)
            ticks = [
                cftime.num2date(dt, self.date_unit, calendar=self.calendar)
                for dt in days
            ]
        elif resolution == "HOURLY":
            hour_unit = "hours since 2000-01-01"
            in_hours = cftime.date2num(
                [lower, upper], hour_unit, calendar=self.calendar
            )
            hours = self._max_n_locator.tick_values(in_hours[0], in_hours[1])
            ticks = [
                cftime.num2date(dt, hour_unit, calendar=self.calendar)
                for dt in hours
            ]
        elif resolution == "MINUTELY":
            minute_unit = "minutes since 2000-01-01"
            in_minutes = cftime.date2num(
                [lower, upper], minute_unit, calendar=self.calendar
            )
            minutes = self._max_n_locator.tick_values(
                in_minutes[0], in_minutes[1]
            )
            ticks = [
                cftime.num2date(dt, minute_unit, calendar=self.calendar)
                for dt in minutes
            ]
        elif resolution == "SECONDLY":
            second_unit = "seconds since 2000-01-01"
            in_seconds = cftime.date2num(
                [lower, upper], second_unit, calendar=self.calendar
            )
            seconds = self._max_n_locator.tick_values(
                in_seconds[0], in_seconds[1]
            )
            ticks = [
                cftime.num2date(dt, second_unit, calendar=self.calendar)
                for dt in seconds
            ]
        else:
            emsg = f"Resolution {resolution} not implemented yet."
            raise ValueError(emsg)
        # Some calenders do not allow a year 0.
        # Remove ticks to avoid raising an error.
        if self.calendar in [
            "proleptic_gregorian",
            "gregorian",
            "julian",
            "standard",
        ]:
            ticks = [t for t in ticks if t.year != 0]
        return cftime.date2num(ticks, self.date_unit, calendar=self.calendar)


class NetCDFTimeConverter(mdates.DateConverter):
    """
    Converter for :py:class:`cftime.datetime` data.

    """

    standard_unit = "days since 2000-01-01"

    @staticmethod
    def axisinfo(unit, axis):
        """
        Returns the :class:`~matplotlib.units.AxisInfo` for *unit*.

        *unit* is a tzinfo instance or None.
        The *axis* argument is required but not used.
        """
        calendar, date_unit, date_type = unit

        majloc = NetCDFTimeDateLocator(4, calendar=calendar)
        majfmt = AutoCFTimeFormatter(majloc, calendar=calendar)
        if date_type is CalendarDateTime:
            datemin = CalendarDateTime(
                cftime.datetime(2000, 1, 1), calendar=calendar
            )
            datemax = CalendarDateTime(
                cftime.datetime(2010, 1, 1), calendar=calendar
            )
        else:
            datemin = date_type(2000, 1, 1)
            datemax = date_type(2010, 1, 1)
        return munits.AxisInfo(
            majloc=majloc,
            majfmt=majfmt,
            label="",
            default_limits=(datemin, datemax),
        )

    @classmethod
    def default_units(cls, sample_point, axis):
        """
        Computes some units for the given data point.

        """
        if hasattr(sample_point, "__iter__"):
            # Deal with nD `sample_point` arrays.
            if isinstance(sample_point, np.ndarray):
                sample_point = sample_point.reshape(-1)
            calendars = np.array([point.calendar for point in sample_point])
            if np.all(calendars == calendars[0]):
                calendar = calendars[0]
            else:
                raise ValueError("Calendar units are not all equal.")
            date_type = type(sample_point[0])
        else:
            # Deal with a single `sample_point` value.
            if not hasattr(sample_point, "calendar"):
                msg = (
                    "Expecting cftimes with an extra " '"calendar" attribute.'
                )
                raise ValueError(msg)
            else:
                calendar = sample_point.calendar
            date_type = type(sample_point)
        if calendar == "":
            raise ValueError(
                "A calendar must be defined to plot dates using a cftime axis."
            )
        return calendar, _TIME_UNITS, date_type

    @classmethod
    def convert(cls, value, unit, axis):
        """
        Converts value, if it is not already a number or sequence of numbers,
        with :py:func:`cftime.date2num`.

        """
        shape = None
        if isinstance(value, np.ndarray):
            # Don't do anything with numeric types.
            if value.dtype != object:
                return value
            shape = value.shape
            value = value.reshape(-1)
            first_value = value[0]
        else:
            # TODO: remove this check once the minimum version of matplotlib
            # supported is at least 3.5, which corresponds to when convert is no
            # longer required to support numeric or iterables of numeric types.
            # See GitHub issue 97 for more details.
            if is_numlike(value):
                return value
            # Not an array but a list of non-numerical types (thus assuming datetime types)
            elif isinstance(value, (list, tuple)):
                first_value = value[0]
            else:
                # Neither numerical, list or ndarray : must be a datetime scalar.
                first_value = value

        if not isinstance(first_value, (CalendarDateTime, cftime.datetime)):
            raise ValueError(
                "The values must be numbers or instances of "
                '"nc_time_axis.CalendarDateTime" or '
                '"cftime.datetime".'
            )

        if isinstance(first_value, CalendarDateTime):
            if not isinstance(first_value.datetime, cftime.datetime):
                raise ValueError(
                    "The datetime attribute of the "
                    "CalendarDateTime object must be of type "
                    "`cftime.datetime`."
                )

        if isinstance(first_value, CalendarDateTime):
            if isinstance(value, (np.ndarray, list, tuple)):
                value = [v.datetime for v in value]
            else:
                value = value.datetime

        result = cftime.date2num(
            value, _TIME_UNITS, calendar=first_value.calendar
        )

        if shape is not None:
            result = result.reshape(shape)

        return result


def is_numlike(x):
    """
    The Matplotlib datalim, autoscaling, locators etc work with scalars which
    are the units converted to floats given the current unit.  The converter may
    be passed these floats, or arrays of them, even when units are set.

    Vendored from matplotlib.units.ConversionInterface.is_numlike.

    TODO: remove this function once the minimum version of matplotlib supported
    by nc-time-axis is at least 3.5.  See GitHub issue 97 for more details.
    """
    if np.iterable(x):
        for thisx in x:
            if thisx is ma.masked:
                continue
            return isinstance(thisx, Number)
    else:
        return isinstance(x, Number)


# Automatically register NetCDFTimeConverter with matplotlib.unit's converter
# dictionary.
if CalendarDateTime not in munits.registry:
    munits.registry[CalendarDateTime] = NetCDFTimeConverter()

CFTIME_TYPES = [
    cftime.datetime,
    cftime.DatetimeNoLeap,
    cftime.DatetimeAllLeap,
    cftime.DatetimeProlepticGregorian,
    cftime.DatetimeGregorian,
    cftime.Datetime360Day,
    cftime.DatetimeJulian,
]
for date_type in CFTIME_TYPES:
    if date_type not in munits.registry:
        munits.registry[date_type] = NetCDFTimeConverter()
