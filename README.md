# nc-time-axis

<h4 align="center">
    Support for a cftime axis in matplotlib
</h4>

<p align="center">

<a href="https://cirrus-ci.com/github/SciTools-/nc-time-axis">
  <img src="https://api.cirrus-ci.com/github/SciTools/nc-time-axis.svg?branch=main"
       alt="cirrus-ci">
</a>
<a href='https://nc-time-axis.readthedocs.io/en/stable/?badge=stable'>
    <img src='https://readthedocs.org/projects/nc-time-axis/badge/?version=stable' alt='Documentation Status' />
</a>
<a href="https://codecov.io/gh/SciTools/nc-time-axis">
  <img src="https://codecov.io/gh/SciTools/nc-time-axis/branch/main/graph/badge.svg?token=JicwCCHwLd"
       alt="codecov">
</a>
<a href="https://results.pre-commit.ci/latest/github/SciTools/nc-time-axis/main">
  <img src="https://results.pre-commit.ci/badge/github/SciTools/nc-time-axis/main.svg"
       alt="pre-commit.ci">
</a>
<a href="https://anaconda.org/conda-forge/nc-time-axis">
  <img src="https://img.shields.io/conda/vn/conda-forge/nc-time-axis?color=orange&label=conda-forge&logo=conda-forge&logoColor=white"
       alt="conda-forge">
</a>
<a href="https://pypi.org/project/nc-time-axis/">
  <img src="https://img.shields.io/pypi/v/nc-time-axis?color=orange&label=pypi&logo=python&logoColor=white"
       alt="pypi">
</a>
<a href="https://github.com/psf/black">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
       alt="black">
</a>
<a href="https://github.com/SciTools/nc-time-axis/blob/main/LICENSE">
  <img src="https://img.shields.io/github/license/SciTools/nc-time-axis?style=plastic"
       alt="license">
</a>
<a href="https://github.com/SciTools/nc-time-axis/graphs/contributors">
  <img src="https://img.shields.io/github/contributors/SciTools/nc-time-axis?style=plastic"
       alt="contributors">
</a>
</p>


## Installation
Install `nc-time-axis` either with `conda`:
```shell
    conda install -c conda-forge nc-time-axis
```
Or `pip`:
```shell
    pip install nc-time-axis
```


## Example

    import random

    import cftime
    import matplotlib.pyplot as plt
    import nc_time_axis

    calendar = "360_day"
    dt = [
        cftime.datetime(year=2017, month=2, day=day, calendar=calendar)
        for day in range(1, 31)
    ]
    temperatures = [round(random.uniform(0, 12), 3) for _ in range(len(dt))]

    plt.plot(dt, temperatures)
    plt.margins(0.1)
    plt.ylim(0, 12)
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.show()

![alt text](https://github.com/SciTools/nc-time-axis/raw/main/example_plot.png "Example plot with cftime axis")


## Reference
* [cftime](https://github.com/Unidata/cftime) - Time-handling functionality from netcdf4-python.
* [matplotlib](http://matplotlib.org/) - Plotting with Python.
