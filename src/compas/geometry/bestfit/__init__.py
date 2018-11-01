from __future__ import print_function, division, absolute_import

from .bestfit import *

import compas
if not compas.is_ironpython():
    from .bestfit_numpy import *


__all__ = [name for name in dir() if not name.startswith('_')]
