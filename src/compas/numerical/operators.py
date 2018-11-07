from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import compas

try:
    from numpy import arange
    from numpy import divide
    from numpy import hstack
    from numpy import tile
    from numpy import asarray

    from scipy import cross
    from scipy.sparse import coo_matrix

except ImportError:
    compas.raise_if_not_ironpython()

from compas.numerical.linalg import normrow
from compas.numerical.linalg import normalizerow
from compas.numerical.linalg import rot90


__all__ = [
    'grad',
    'div',
    'curl'
]


def grad(V, F, rtype='array'):
    """Construct the gradient operator of a trianglular mesh.

    Parameters
    ----------
    V : array
        Vertex coordinates of the mesh.
    F : array
        Face vertex indices of the mesh.
    rtype : {'array', 'csc', 'csr', 'coo', 'list'}
        Format of the result.

    Returns
    -------
    array-like
        Depending on rtype return type.

    Notes
    -----
    The gradient operator is fully determined by the connectivity of the mesh
    and the coordinate difference vectors associated with the edges

    """
    v = V.shape[0]
    f = F.shape[0]

    f0 = F[:, 0]  # Index of first vertex of each face
    f1 = F[:, 1]  # Index of second vertex of each face
    f2 = F[:, 2]  # Index of last vertex of each face

    e01 = V[f1, :] - V[f0, :]  # Vector from vertex 0 to 1 for each face
    e12 = V[f2, :] - V[f1, :]  # Vector from vertex 1 to 2 for each face
    e20 = V[f0, :] - V[f2, :]  # Vector from vertex 2 to 0 for each face

    n = cross(e12, e20)  # Normal vector to each face
    A2 = normrow(n)      # Length of normal vector is twice the area of the face
    u = normalizerow(n)  # Unit normals for each face

    e01_ = divide(cross(u, e01), A2)  # Vector perpendicular to v01, normalized by A2
    e20_ = divide(cross(u, e20), A2)  # Vector perpendicular to v20, normalized by A2

    i = hstack((  # Nonzero rows
        0 * f + tile(arange(f), (1, 4)),
        1 * f + tile(arange(f), (1, 4)),
        2 * f + tile(arange(f), (1, 4))
    )).flatten()

    j = tile(hstack((f1, f0, f2, f0)), (1, 3)).flatten()  # Nonzero columns

    data = hstack((
        hstack((e20_[:, 0], - e20_[:, 0], e01_[:, 0], - e01_[:, 0])),
        hstack((e20_[:, 1], - e20_[:, 1], e01_[:, 1], - e01_[:, 1])),
        hstack((e20_[:, 2], - e20_[:, 2], e01_[:, 2], - e01_[:, 2])),
    )).flatten()

    G = coo_matrix((data, (i, j)), shape=(3 * f, v))

    if rtype == 'array':
        return G.toarray()
    elif rtype == 'csr':
        return G.tocsr()
    elif rtype == 'csc':
        return G.tocsc()
    elif rtype == 'coo':
        return G
    else:
        return G


def div():
    raise NotImplementedError


def curl():
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    import compas
    from compas.datastructures import Mesh
    from compas.datastructures import mesh_quads_to_triangles
    from compas.geometry import add_vectors
    from compas.plotters import MeshPlotter
    from compas.utilities import i_to_blue

    mesh = Mesh.from_obj(compas.get('hypar.obj'))

    mesh_quads_to_triangles(mesh)

    vertices, faces = mesh.to_vertices_and_faces()

    V = asarray(vertices)
    F = asarray(faces, dtype=int)

    G = grad(V, F, 'csr')
    Z = V[:, 2].reshape((-1, 1))

    g = - G.dot(Z)

    vectors = g.reshape((F.shape[0], 3), order='F').tolist()

    lines = []
    for vector, fkey in zip(vectors, mesh.faces()):
        start = mesh.face_centroid(fkey)
        end = add_vectors(start, vector)

        lines.append({
            'start' : start,
            'end'   : end,
            'arrow' : 'end',
            'color' : '#ff0000'
        })

    z = mesh.get_vertices_attribute('z')
    zmin = min(z)
    zmax = max(z)
    zrange = zmax - zmin

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(radius=0.05, facecolor={key: i_to_blue((attr['z'] - zmin) / zrange) for key, attr in mesh.vertices(True)})
    plotter.draw_edges()
    plotter.draw_faces()

    plotter.draw_arrows(lines)

    plotter.show()
