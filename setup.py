import os
import os.path
from setuptools import setup

import versioneer


here = os.path.abspath(os.path.dirname(__file__))
packages = []
for d, _, _ in os.walk(os.path.join(here, 'nc_time_axis')):
    if os.path.exists(os.path.join(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))

setup_args = dict(
    name='nc-time-axis',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='cftime support for matplotlib axis',
    license='BSD3',
    author='Laura Dreyer, Philip Elson',
    url='https://github.com/scitools/nc-time-axis',
    packages=packages,
    install_requires = ['cftime',
                        'matplotlib',
                        'numpy',
                        'six'],
    tests_require = ['mock', 'pep8'],
    test_suite='nc_time_axis.tests'
)

if __name__ == '__main__':
    setup(**setup_args)
