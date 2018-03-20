from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_split_edge',
    'mesh_split_face',
    'trimesh_split_edge',
]


def mesh_split_edge(self, u, v, t=0.5, allow_boundary=False):
    """Split and edge by inserting a vertex along its length.

    Parameters
    ----------
    u : str
        The key of the first vertex of the edge.
    v : str
        The key of the second vertex of the edge.
    t : float (0.5)
        The position of the inserted vertex.
        The value should be between 0.0 and 1.0
    allow_boundary : bool (False)
        Split edges on the boundary.

    Returns
    -------
    int
        The key of the inserted vertex.

    Raises
    ------
    ValueError
        If u and v are not neighbours.

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = self.halfedge[u][v]
    fkey_vu = self.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = self.edge_point(u, v, t)

    # the split vertex
    w = self.add_vertex(x=x, y=y, z=z)

    # split half-edge UV
    self.halfedge[u][w] = fkey_uv
    self.halfedge[w][v] = fkey_uv
    del self.halfedge[u][v]

    # update the UV face if it is not the `None` face
    if fkey_uv is not None:
        j = self.face[fkey_uv].index(v)
        self.face[fkey_uv].insert(j, w)

    # split half-edge VU
    self.halfedge[v][w] = fkey_vu
    self.halfedge[w][u] = fkey_vu
    del self.halfedge[v][u]

    # update the VU face if it is not the `None` face
    if fkey_vu is not None:
        i = self.face[fkey_vu].index(u)
        self.face[fkey_vu].insert(i, w)

    return w


def trimesh_split_edge(self, u, v, t=0.5, allow_boundary=False):
    """Split an edge of a triangle mesh.

    Parameters
    ----------
    u : hashable
        Identifier of the first vertex.
    v : hashable
        Identifier of the second vertex.
    t : float (0.5)
        The location of the split point along the original edge.
        The value should be between 0.0 and 1.0
    allow_boundary : bool (False)
        Allow splits on boundary edges.

    Notes
    -----
    This operation only works as expected for triangle meshes.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.plotters import MeshPlotter
        from compas.topology import mesh_quads_to_triangles

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        mesh_quads_to_triangles(mesh)

        split = mesh.split_edge_tri(17, 30)

        facecolor = {key: '#cccccc' if key != split else '#ff0000' for key in mesh.vertices()}

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2, facecolor=facecolor)
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

        plotter.show()

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = self.halfedge[u][v]
    fkey_vu = self.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = self.edge_point(u, v, t)

    # the split vertex
    w = self.add_vertex(x=x, y=y, z=z)

    # the UV face
    if fkey_uv is None:
        self.halfedge[u][w] = None
        self.halfedge[w][v] = None
        del self.halfedge[u][v]
    else:
        face = self.face[fkey_uv]
        o = face[face.index(u) - 1]
        self.add_face([u, w, o])
        self.add_face([w, v, o])
        del self.halfedge[u][v]
        del self.face[fkey_uv]

    # the VU face
    if fkey_vu is None:
        self.halfedge[v][w] = None
        self.halfedge[w][u] = None
        del self.halfedge[v][u]
    else:
        face = self.face[fkey_vu]
        o = face[face.index(v) - 1]
        self.add_face([v, w, o])
        self.add_face([w, u, o])
        del self.halfedge[v][u]
        del self.face[fkey_vu]

    # return the key of the split vertex
    return w


def mesh_split_face(self, fkey, u, v):
    """Split a face by inserting an edge between two specified vertices.

    Parameters:
        fkey (str) : The face key.
        u (str) : The key of the first split vertex.
        v (str) : The key of the second split vertex.

    """
    if u not in self.face[fkey] or v not in self.face[fkey]:
        raise ValueError('The split vertices do not belong to the split face.')

    face = self.face[fkey]

    i = face.index(u)
    j = face.index(v)

    if i + 1 == j:
        raise ValueError('The split vertices are neighbours.')

    if j > i:
        f = face[i:j + 1]
        g = face[j:] + face[:i + 1]
    else:
        f = face[i:] + face[:j + 1]
        g = face[j:i + 1]

    f = self.add_face(f)
    g = self.add_face(g)

    del self.face[fkey]

    return f, g


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter
    from compas.topology import mesh_quads_to_triangles

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh_quads_to_triangles(mesh)

    split = mesh.split_edge_tri(15, 20)

    facecolor = {key: '#cccccc' if key != split else '#ff0000' for key in mesh.vertices()}

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2, facecolor=facecolor)
    plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

    plotter.show()
