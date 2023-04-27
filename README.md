# nc-time-axis

<h4 align="center">
    Support for a <a href="https://github.com/Unidata/cftime">cftime</a> axis in <a href="http://matplotlib.org/">matplotlib</a>
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

```python
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
```

![alt text](https://github.com/SciTools/nc-time-axis/raw/main/example_plot.png "Example plot with cftime axis")


## License

`nc-time-axis` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.


## [#ShowYourStripes](https://showyourstripes.info/s/globe)

<h4 align="center">
  <a href="https://showyourstripes.info/s/globe">
    <img src="https://raw.githubusercontent.com/ed-hawkins/show-your-stripes/master/2021/GLOBE---1850-2021-MO.png"
         height="50" width="800"
         alt="#showyourstripes Global 1850-2021"></a>
</h4>

**Graphics and Lead Scientist**: [Ed Hawkins](http://www.met.reading.ac.uk/~ed/home/index.php), National Centre for Atmospheric Science, University of Reading.

**Data**: Berkeley Earth, NOAA, UK Met Office, MeteoSwiss, DWD, SMHI, UoR, Meteo France & ZAMG.

<p>
<a href="https://showyourstripes.info/s/globe">#ShowYourStripes</a> is distributed under a
<a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
<a href="https://creativecommons.org/licenses/by/4.0/">
  <img src="https://i.creativecommons.org/l/by/4.0/80x15.png" alt="creative-commons-by" style="border-width:0"></a>
</p>
