from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from collections import deque
from compas.topology import breadth_first_traverse


__all__ = [
    'connected_components',
    'mesh_is_connected',
    'network_is_connected',
]


def connected_components(adjacency):
    """Identify the vertices of connected components.

    Parameters
    ----------
    adjacency : dict
        An adjacency dictionary mapping vertex identifiers to neighbours.

    Returns
    -------
    list of list of hashable
        A nested list of vertex identifiers.

    Examples
    --------
    .. code-block:: python

        pass

    """
    tovisit = set(adjacency)
    components = []
    while tovisit:
        root = tovisit.pop()
        visited = breadth_first_traverse(adjacency, root)
        tovisit -= visited
        components.append(list(visited))
    return components


def mesh_is_connected(mesh):
    """Verify that the mesh is connected.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh data structure.

    Returns
    -------
    bool
        True, if the mesh is connected.
        False, otherwise.

    Notes
    -----
    A mesh is connected if for every two vertices a path exists connecting them.

    """
    if not mesh.vertex:
        return False

    nodes = breadth_first_traverse(mesh.adjacency, mesh.get_any_vertex())

    return len(nodes) == mesh.number_of_vertices()


def network_is_connected(network):
    """Verify that the network is connected.

    Returns
    -------
    bool
        True, if the network is connected.
        False, otherwise.

    Notes
    -----
    A network is connected if for every two vertices a path exists connecting them.

    """
    if not network.vertex:
        return False

    nodes = breadth_first_traverse(network.adjacency, network.get_any_vertex())

    return len(nodes) == network.number_of_vertices()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network
    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('grid_irregular.obj'))

    components = connected_components(network.adjacency)

    key_color = vertex_coloring(network.adjacency)

    colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00']

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.draw_vertices(facecolor={key: colors[key_color[key]] for key in network.vertices()})
    plotter.draw_edges()

    plotter.show()
