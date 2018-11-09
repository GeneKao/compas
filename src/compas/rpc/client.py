from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import time
import json

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy

from subprocess import Popen

import compas

from compas.datastructures import Datastructure
from compas.rpc import RPCServerError


__all__ = ['Client']


class Client(object):

    def __init__(self, package=None):
        self._package = package
        self._funcname = None
        self._func = None
        self._process = None
        self._python = 'pythonw'
        self._port = 8888
        self._url = 'http://127.0.0.1'
        self._service = 'default.py'
        self._server = None
        self.profile = None
        self.stop_server()
        self.start_server()

    def __del__(self):
        self.stop_server()

    def start_server(self):
        python = self._python
        script = os.path.join(compas.HOME, 'services', self._service)
        address = "{}:{}".format(self._url, self._port)

        self._process = Popen([python, script])
        self._server = ServerProxy(address)

        success = False
        count = 100
        while count:
            try:
                self._server.ping()
            except:
                time.sleep(0.01)
                count -= 1
            else:
                success = True
                break
        if not success:
            raise RPCServerError("The server is no available.")

    def stop_server(self):
        try:
            self._server.kill()
        except:
            pass
        try:
            self._process.terminate()
        except:
            pass
        try:
            self._process.kill()
        except:
            pass

    def __getattr__(self, funcname):
        self._funcname = funcname

        try:
            self._func = getattr(self._server, self._funcname)
        except:
            raise RPCServerError("This function is not available: {}".format(funcname))

        return self.func 

    def func(self, *args, **kwargs):
        try:
            result = self._func(*args, **kwargs)
        except:
            self.stop_server()
            raise

        if not result:
            raise RPCServerError("No output was generated.")

        return result


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    
    import compas

    from compas.datastructures import Mesh
    from compas_rhino.artists import MeshArtist

    from compas.rpc import Client

    client = Client('compas.numerical')

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'is_fixed': False, 'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})
    mesh.set_vertices_attribute('is_fixed', True, keys=mesh.vertices_where({'vertex_degree': 2}))

    data = client.mesh_fd_numpy(json.dumps(mesh.to_data()))
    mesh.data = json.loads(data)

    artist = MeshArtist(mesh, layer='Mesh')

    artist.clear_layer()
    artist.draw_vertices()
    artist.draw_faces()

    artist.redraw()
