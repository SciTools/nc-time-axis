.. _examples:

.. currentmodule:: nc_time_axis

Examples
========

Basic usage
-----------

nc-time-axis works by adding converters to matplotlib's flexible `units registry
<https://matplotlib.org/stable/api/units_api.html>`_.  To register its
converters, simply import nc-time-axis.  Then you will be able to make plots
with :py:class:`cftime.datetime` axes.

.. ipython:: python
    :okwarning:

    import cftime
    import matplotlib.pyplot as plt
    import nc_time_axis
    import numpy as np

    fig, ax = plt.subplots(1, 1)
    x = np.linspace(0, 6 * np.pi)
    y = 0.5 * x + np.sin(x)
    times = cftime.num2date(x, units="days since 2000-01-01", calendar="noleap")
    ax.plot(times, y);

    @savefig basic.png
    fig.show()

Setting the axes ticks and tick format
--------------------------------------

In the first example, the ticks and tick label formats were chosen automatically
using heuristics in nc-time-axis.  If you would like to explicitly set the tick
positions and label format you may do so using
:py:meth:`matplotlib.axes.Axes.set_xticks` and :py:class:`CFTimeFormatter`.  The
:py:class:`CFTimeFormatter` takes in a date format string (see `the Python
documentation
<https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_
for acceptable format codes) and the calendar type of the axis (see
the :py:class:`cftime.datetime` documentation for valid calendar strings).

.. ipython:: python
    :okwarning:

    fig, ax = plt.subplots(1, 1)
    ax.plot(times, y);
    ax.set_xticks([cftime.datetime(2000, 1, day, calendar="noleap") for day in range(2, 19, 4)]);
    formatter = nc_time_axis.CFTimeFormatter("%m-%d %H:%M", "noleap")
    ax.xaxis.set_major_formatter(formatter)

    @savefig set_ticks.png
    fig.show()
