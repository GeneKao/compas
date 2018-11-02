"""
********************************************************************************
compas
********************************************************************************

.. currentmodule:: compas


.. toctree::
    :maxdepth: 1

    compas.datastructures
    compas.files
    compas.geometry
    compas.numerical
    compas.plotters
    compas.robots
    compas.topology
    compas.utilities

..
    compas.viewers

"""

from __future__ import print_function, division, absolute_import

import os
import sys

from ._os import *
from ._data import *

PY3 = sys.version_info[0] == 3

PRECISION = '3f'

IPY = is_ironpython()


__author__    = 'Tom Van Mele and many others (see CONTRIBUTORS.md)'
__copyright__ = 'Copyright 2014-2018 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'
__version__   = '0.3.4'


__all__ = []


def license():
    with open(os.path.join(HOME, 'LICENSE')) as fp:
        return fp.read()


def version():
    return __version__


def help():
    return 'http://compas-dev.github.io'


def copyright():
    return __copyright__


def verify():
    requirements = [
        'numpy',
        'scipy',
        'matplotlib',
    ]
    optional = [
        'cvxopt',
        'cvxpy',
        'Cython',
        'imageio',
        'networkx',
        'numba',
        'pandas',
        'paramiko',
        'pycuda',
        'PyOpenGL',
        'PySide',
        'Shapely',
        'sympy',
    ]
    current = installed()

    print('=' * 80)
    print('Checking required packages...\n')
    issues = []
    for package in requirements:
        if package not in current:
            issues.append(package)
    if issues:
        print('The following required packages are not installed:')
        for package in issues:
            print('- {}'.format(package))
    else:
        print('All required packages are installed.')

    print('\nChecking optional packages...\n')
    issues = []
    for package in optional:
        if package not in current:
            issues.append(package)
    if issues:
        print('The following optional packages are not installed:')
        for package in issues:
            print('- {}'.format(package))
    else:
        print('All optional packages are installed.')
    print('=' * 80)
    print()


def installed():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    flat_installed_packages = [package.project_name for package in installed_packages]
    return sorted(flat_installed_packages, key=str.lower)


def requirements():
    with open(os.path.join(HERE, '../requirements.txt')) as f:
        for line in f:
            print(line.strip())

