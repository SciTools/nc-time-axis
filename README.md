# nc-time-axis

<h4 align="center">
    Support for a <a href="https://github.com/Unidata/cftime">cftime</a> axis in matplotlib
</h4>


|                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ⚙️ CI            | [![ci-citation](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-citation.yml/badge.svg)](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-citation.yml) [![ci-locks](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-locks.yml/badge.svg)](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-locks.yml) [![ci-manifest](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-manifest.yml/badge.svg)](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-manifest.yml) [![ci-wheels](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-wheels.yml/badge.svg)](https://github.com/SciTools/nc-time-axis/actions/workflows/ci-wheels.yml) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/SciTools/nc-time-axis/main.svg)](https://results.pre-commit.ci/latest/github/SciTools/nc-time-axis/main) |
| 💬 Community     | [![GH Discussions](https://img.shields.io/badge/github-discussions%20%F0%9F%92%AC-yellow?logo=github&logoColor=lightgrey)](https://github.com/SciTools/nc-time-axis/discussions)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 📖 Documentation | [![RTD Status](https://readthedocs.org/projects/nc-time-axis/badge/?version=stable)](https://nc-time-axis.readthedocs.io/en/stable/?badge=stable)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 📈 Health        | [![codecov](https://codecov.io/gh/SciTools/nc-time-axis/branch/master/graph/badge.svg?token=JicwCCHwLd)](https://codecov.io/gh/SciTools/nc-time-axis)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ✨ Meta           | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![license - bds-3-clause](https://img.shields.io/github/license/SciTools/nc-time-axis)](https://github.com/SciTools/nc-time-axis/blob/main/LICENSE)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 📦 Package       | [![conda-forge](https://img.shields.io/conda/vn/conda-forge/nc-time-axis?color=orange&label=conda-forge&logo=conda-forge&logoColor=white)](https://anaconda.org/conda-forge/nc-time-axis) [![pypi](https://img.shields.io/pypi/v/nc-time-axis?color=orange&label=pypi&logo=python&logoColor=white)](https://pypi.org/project/nc-time-axis/) [![pypi - python version](https://img.shields.io/pypi/pyversions/nc-time-axis.svg?color=orange&logo=python&label=python&logoColor=white)](https://pypi.org/project/nc-time-axis/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6472640.svg)](https://doi.org/10.5281/zenodo.6472640)                                                                                                                                                                                                                                                                   |
| 🧰 Repo          | [![contributors](https://img.shields.io/github/contributors/SciTools/nc-time-axis)](https://github.com/SciTools/nc-time-axis/graphs/contributors)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|                  |


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


## License

`nc-time-axis` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
