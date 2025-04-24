.. _api:

.. currentmodule:: nc_time_axis

API reference
=============

This page provides a reference for the API of nc-time-axis.

CalendarDateTime
----------------

For historical reasons, nc-time-axis defines a :py:class:`CalendarDateTime`
class which encapsulates a :py:class:`cftime.datetime` object and its calendar
type.  This is no longer needed, and will be removed in nc-time-axis version
1.5, but we document it here for now.

.. autosummary::
    :toctree: _api_generated/

    CalendarDateTime

Formatters
----------

The :py:class:`AutoCFTimeFormatter` is what is used by default when plotting
:py:class:`cftime.datetime` axis; it will automatically pick a date label format
depending on the axis range.  If you would like more control over the format of
the date labels you may use the :py:class:`CFTimeFormatter` class.

.. autosummary::
    :toctree: _api_generated/

    AutoCFTimeFormatter
    CFTimeFormatter

Locators
--------

The :py:class:`NetCDFTimeDateLocator` is what is used by default to set the tick
locations depending on the range of the axis.  For finer-grained control over
the tick locations, use matplotlib's :py:meth:`matplotlib.axes.Axes.set_xticks`
or :py:meth:`matplotlib.axes.Axes.set_yticks` methods to set the tick locations
explicitly.

.. autosummary::
    :toctree: _api_generated/

    NetCDFTimeDateLocator

Converters
----------

Internally, nc-time-axis must convert times to numerical values so that
matplotlib can plot them on axes.  The :py:class:`NetCDFTimeConverter` is used
for this purpose.

.. autosummary::
    :toctree: _api_generated/

    NetCDFTimeConverter
