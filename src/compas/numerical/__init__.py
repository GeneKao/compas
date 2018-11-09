"""
********************************************************************************
compas.numerical
********************************************************************************

.. currentmodule:: compas.numerical


Algorithms
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DynamicRelaxation
    DynamicRelaxationX
    ForceDensity


.. autosummary::
    :toctree: generated/
    :nosignatures:

    pca_numpy
    topop2d_numpy
    topop3d_numpy


Solvers
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    descent
    devo_numpy
    ga
    moga


Functions
=========

**linalg**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    nullspace
    rank
    dof
    pivots
    nonpivots
    rref
    rref_sympy
    rref_matlab
    chofactor
    lufactorized
    uvw_lengths
    normrow
    normalizerow
    rot90
    solve_with_known
    spsolve_with_known


**matrices**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_matrix
    degree_matrix
    connectivity_matrix
    laplacian_matrix
    face_matrix
    mass_matrix
    equilibrium_matrix
    network_adjacency_matrix
    network_degree_matrix
    network_connectivity_matrix
    network_laplacian_matrix
    mesh_adjacency_matrix
    mesh_degree_matrix
    mesh_face_matrix
    mesh_connectivity_matrix
    mesh_laplacian_matrix
    trimesh_cotangent_laplacian_matrix


**operators**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    grad


Utilities
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    float_formatter
    set_array_print_precision
    unset_array_print_precision


"""
from __future__ import print_function, division, absolute_import

from .utilities import *
from .matrices import *

from .linalg import *
from .operators import *

from .descent import *
from .devo import *
from .dr import *
from .drx import *
from .fd import *
from .ga import *
from .lma import *
from .mma import *
from .pca import *
from .topop import *

__all__ = [name for name in dir() if not name.startswith('_')]
