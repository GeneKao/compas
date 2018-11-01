from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

from ._os import *


HERE = os.path.dirname(__file__)
HOME = absjoin(HERE, '../..')
DATA = absjoin(HERE, '../../data')
TEMP = absjoin(HERE, '../../temp')

APPDATA = user_data_dir('COMPAS', 'compas-dev', roaming=True)
APPTEMP = absjoin(APPDATA, 'temp')


__all__ = ['get', 'get_bunny', ]


def get(filename):
    """Get the full path to one of the sample data files.

    Parameters
    ----------
    filename : str
        The name of the data file.
        The following are available.

        * boxes.obj
        * faces.obj
        * fink.obj
        * hypar.obj
        * lines.obj
        * saddle.obj

    Returns
    -------
    str
        The full path to the specified file.

    Notes
    -----
    The file name should be specified relative to the **COMPAS** sample data folder.
    This folder is only locally available if you installed **COMPAS** from source,
    or if you are working directly with the source.
    In all other cases, the function will get the corresponding files direcly from
    the GitHub repo, at https://raw.githubusercontent.com/compas-dev/compas/master/data

    Examples
    --------
    The ``compas.get`` function is meant to be used in combination with the static
    constructors of the data structures.

    .. code-block:: python

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_obj(compas.get('faces.obj'))

    """
    filename = filename.strip('/')

    if filename.endswith('bunny.ply'):
        return get_bunny()

    localpath = absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath
    else:
        return "https://raw.githubusercontent.com/compas-dev/compas/master/data/{}".format(filename)


def get_bunny(localstorage=None):
    """Get the *Stanford Bunny* directly from the Stanford repository.

    Parameters
    ----------
    localstorage : str, optional
        Path to a local storage folder for saving the downloaded data.
        Default is ``None``, in which case the data will be stored in a local
        user data directory. See https://pypi.org/project/appdirs/ for more info.

    Returns
    -------
    str
        Full path to the local file.

    Examples
    --------
    The *Stanford Bunny* is a `PLY` file.
    Therefore, the returned path should be used in combination with the ``PLY``
    file reader, or with the ``from_ply`` constructor function for meshes.

    .. code-block:: python

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_ply(compas.get_bunny())

    """
    import tarfile

    try:
        from urllib.request import urlretrieve
    except ImportError:
        from urllib import urlretrieve

    if not localstorage:
        localstorage = APPDATA

    if not os.path.exists(localstorage):
        os.makedirs(localstorage)

    if not os.path.isdir(localstorage):
        raise Exception('Local storage location does not exist: {}'.format(localstorage))

    if not os.access(localstorage, os.W_OK):
        raise Exception('Local storage location is not writable: {}'.format(localstorage))

    bunny = compas._os.absjoin(localstorage, 'bunny/reconstruction/bun_zipper.ply')
    destination = compas._os.absjoin(localstorage, 'bunny.tar.gz')

    if not os.path.exists(bunny):
        url = 'http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz'

        print('Getting the bunny from {} ...'.format(url))
        print('This will take a few seconds...')

        urlretrieve(url, destination)

        with tarfile.open(destination) as file:
            file.extractall(localstorage)

        os.remove(destination)

        print('Got it!\n')

    return bunny
