.. _release_notes:

.. currentmodule:: nc_time_axis

Release notes
=============

v1.4.1 (April 20th, 2022)
-------------------------

New features
~~~~~~~~~~~~
* Starting with this release, every new releasgit re of nc-time-axis will be
  associated with a Digital Object Identifier (DOI) through Zenodo, making it
  easier to cite in academic articles (:issue:`104`).  By `Spencer Clark
  <https://github.com/spencerkclark>`_.

Bug fixes
~~~~~~~~~
* As of matplotlib version 3.5, unit converters no longer need to support
  passing numeric or iterables of numeric values to their ``convert`` method.
  Accordingly, the :py:meth:`matplotlib.units.ConversionInterface.is_numlike`
  method has been deprecated.  For backwards compatibility with older versions
  of matplotlib, we have vendored this function for the time being, but will
  remove it once the minimum version of matplotlib supported by nc-time-axis is
  at least 3.5 (:issue:`97`, :pull:`106`).  By `Spencer Clark
  <https://github.com/spencerkclark>`_.

Infrastructure
~~~~~~~~~~~~~~
* Update usage of ``conda-lock`` in continuous integration to continue to create
  lockfiles that can be used to create mamba environments (:pull:`107`).  By
  `Spencer Clark <https://github.com/spencerkclark>`_ and `Ruth Comer
  <https://github.com/rcomer>`_.


v1.4.0 (October 23rd, 2021)
---------------------------

Deprecations
~~~~~~~~~~~~ 

* The :py:class:`CalendarDateTime` class has been deprecated and will be removed
  in nc-time-axis version 1.5.0. Please switch to plotting instances or
  subclasses of :py:class:`cftime.datetime` directly (:issue:`62`, :pull:`87`).
  See the :ref:`examples` for illustration.  By `Spencer Clark
  <https://github.com/spencerkclark>`_.

New features
~~~~~~~~~~~~

* Added a :py:class:`CFTimeFormatter` class to enable custom formatting for
  :py:class:`cftime.datetime` ticks (:issue:`41`, :pull:`84`).  By `Spencer
  Clark <https://github.com/spencerkclark>`_.
* Added ability to plot calendar-aware :py:class:`cftime.datetime` objects, e.g.
  ``cftime.datetime(2000, 1, 1, calendar="noleap")``, available as of cftime
  version 1.3.0 (:issue:`75`, :pull:`80`).  By `Spencer Clark
  <https://github.com/spencerkclark>`_.

Bug fixes
~~~~~~~~~

* Enabled :py:meth:`NetCDFTimeConverter.convert` to take a :py:class:`list` of
  datetimes as an argument, allowing matplotlib methods like
  :py:meth:`matplotlib.axes.Axes.axvspan` and
  :py:meth:`matplotlib.axes.Axes.fill_between` to work properly with cftime
  values (:issue:`47`, :issue:`74`, :pull:`78`).  By `Pascal Bourgault
  <https://github.com/aulemahal>`_.
* Fixed a bug that resulted in the resolution of tick labels being inconsistent 
  with the resolution of tick values (:issue:`48`, :pull:`79`).  By `Spencer
  Clark <https://github.com/spencerkclark>`_.
* Fixed a bug that prevented users from being able to explicitly set the ticks 
  along axes using :py:meth:`matplotlib.axes.Axes.set_xticks` or
  :py:meth:`matplotlib.axes.Axes.set_yticks` (:issue:`41`, :pull:`84`).  By
  `Spencer Clark <https://github.com/spencerkclark>`_.

Documentation
~~~~~~~~~~~~~

* Added a start on Read the Docs documentation.  Added examples, release notes,
  and NumPy-style docstrings to nc-time-axis classes (:issue:`62`, :pull:`87`).
  By `Spencer Clark <https://github.com/spencerkclark>`_.
* Added some basic instructions for making a new release (:pull:`94`).  By
  `Spencer Clark <https://github.com/spencerkclark>`_.


v1.3.1 (June 14th, 2021)
------------------------

Requirements
~~~~~~~~~~~~

* nc-time-axis now requires cftime of at least version 1.5 (:discussion:`61`,
  :pull:`69`).  By `Bill Little <https://github.com/bjlittle>`_.


v1.3.0 (June 11th, 2021)
------------------------

Requirements
~~~~~~~~~~~~

* Support for Python 2 was dropped.

Infrastructure
~~~~~~~~~~~~~~

* Migrated continuous integration from Travis CI to Cirrus CI through GitHub
  Actions.  Added formatting and linting checks.  Updated packaging to use
  `setuptools <https://setuptools.readthedocs.io/en/latest/>`_.  Added issue and
  pull request templates.  Enabled GitHub discussions.  For more details see
  :issue:`63` and :pull:`66`.  By `Bill Little <https://github.com/bjlittle>`_.
* Changed the name of the primary branch from "master" to "main" (:pull:`68`).
  By `Bill Little <https://github.com/bjlittle>`_.

Bug fixes
~~~~~~~~~

* Removed ticks with year zero in calendars without year zero.  Previously these
  would lead to errors in cftime, which would prevent plotting (:issue:`44`,
  :pull:`50`).  By `Julius Busecke <https://github.com/jbusecke>`_.
* Removed internal use of the deprecated :py:class:`cftime.utime` class
  (:pull:`59` through :pull:`66`).  By `Pascal Bourgault
  <https://github.com/aulemahal>`_.
* Removed internal use of the deprecated :py:class:`numpy.object` data type
  (:pull:`56` through :pull:`66`).  By `Mathias Hauser
  <https://github.com/mathause>`_.
* Updated internals for compatibility with the now calendar-aware
  :py:class:`cftime.datetime` object (:pull:`51` through :pull:`66`).  By `Jeff
  Whitaker <https://github.com/jswhit>`_.
* Improved handling of scalar values passed to
  :py:meth:`NetCDFTimeConverter.convert` (:issue:`45`, :pull:`46`).  By `Spencer
  Clark <https://github.com/spencerkclark>`_.


v1.2.0 (January 25th, 2019)
---------------------------

Infrastructure
~~~~~~~~~~~~~~

* Included license in package data (:pull:`37`).  By `Filipe Fernandes
  <https://github.com/ocefpaf>`_.

New features
~~~~~~~~~~~~

* Added ability to directly plot subclasses of :py:class:`cftime.datetime`, e.g.
  :py:class:`cftime.DatetimeNoLeap`, instead of requiring
  :py:class:`CalendarDateTime` objects (:pull:`42`).  By `Spencer
  Clark <https://github.com/spencerkclark>`_.


v1.1.0 (May 31st, 2018)
-----------------------

Requirements
~~~~~~~~~~~~

* nc-time-axis now requires matplotlib of at least version 2.0 (:issue:`23`,
  :pull:`34`).  By `Filipe Fernandes <https://github.com/ocefpaf>`_.
* nc-time-axis now uses the standalone cftime package instead of the
  ``netcdftime`` module formerly packaged in netcdf4-python (:pull:`30`,
  :pull:`32`). By `Filipe Fernandes <https://github.com/ocefpaf>`_.

Infrastructure
~~~~~~~~~~~~~~

* Updated continuous integration tests to be run with both Python 2 and Python 3
  (:pull:`33`).  By `Filipe Fernandes <https://github.com/ocefpaf>`_.
* Updated continuous integration to use ``install_requires`` information to
  install dependencies of nc-time-axis instead of a requirements file
  (:issue:`27`, :pull:`28`).  By `Phil Elson <https://github.com/pelson>`_.
* Added installation and test requirements to ``setup.py`` (:pull:`26`).  By
  `Luke Carroll <https://github.com/LukeC92>`_.

Documentation
~~~~~~~~~~~~~

* Added installation instructions and a usage example to the README for display
  on GitHub (:pull:`24`, :pull:`25`).  By `mbeedie
  <https://github.com/mbeedie>`_.


v1.0.2 (March 7th, 2017)
------------------------

Requirements
~~~~~~~~~~~~

* nc-time-axis now requires matplotlib less than version 2.0 (:pull:`22`).  By
  `Mark Hedley <https://github.com/marqh>`_.

Bug fixes
~~~~~~~~~

* Fixed a bug in comparing calendars (:pull:`22`).  By `Mark
  Hedley <https://github.com/marqh>`_.


v1.0.1 (November 23rd, 2016)
----------------------------

Bug fixes
~~~~~~~~~

* Fixed a bug the prevented converting NumPy arrays of datetime objects.  This
  enables making Hovmoller diagrams using nc-time-axis.  By `Peter Killick
  <https://github.com/DPeterK>`_.


v1.0.0 (July 1st, 2016)
-----------------------

This is the initial release of the nc-time-axis package.  It is based on a
prototype written by `Phil Elson <https://github.com/pelson>`_, which was made
production-ready by `lbdreyer <https://github.com/lbdreyer>`_.

New features
~~~~~~~~~~~~

* Added the fundamental objects of nc-time-axis, i.e.
  :py:class:`NetCDFTimeDateLocator`, :py:class:`NetCDFTimeDateFormatter`, and
  :py:class:`NetCDFTimeConverter` (:pull:`2`).  By `lbdreyer
  <https://github.com/lbdreyer>`_ and `Phil Elson <https://github.com/pelson>`_.
* Added unit and integration tests (:pull:`3`, :pull:`13`).  By `lbdreyer
  <https://github.com/lbdreyer>`_.
* Added a ``__version__`` attribute to nc-time-axis (:pull:`9`).  By `lbdreyer
  <https://github.com/lbdreyer>`_.
* Added the :py:class:`CalendarDateTime` class (:pull:`12`, :pull:`15`).  By
  `lbdreyer <https://github.com/lbdreyer>`_.

Infrastructure
~~~~~~~~~~~~~~

* Added initial packaging infrastructure (:pull:`4`).  By `lbdreyer
  <https://github.com/lbdreyer>`_.
* Configured continuous integration to be run using Travis CI (:pull:`6`).  By
  `lbdreyer <https://github.com/lbdreyer>`_.
* Added test coverage computation and reporting (:pull:`17`, :pull:`19`). By
  `lbdreyer <https://github.com/lbdreyer>`_.

Documentation
~~~~~~~~~~~~~

* Added a Travis CI badge to the README and convert to reStructuredText format
  (:pull:`11`).  By `lbdreyer <https://github.com/lbdreyer>`_.
* Added basic description to the README (:pull:`5`).  By `Peter Killick
  <https://github.com/DPeterK>`_.
* Added contributing guidelines to the repository (:pull:`1`).  By
  `lbdreyer <https://github.com/lbdreyer>`_.
