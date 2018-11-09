from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

try:
    import cProfile as Profile
except ImportError:
    import profile as Profile

import pstats
import traceback


__all__ = ['Service']


class Service(object):

    def _dispatch(self, name, args):
        try:
            method = getattr(self, name)
        except AttributeError:
            return 'The requested method is not part of the API: {0}.'.format(name)

        try:
            idict = json.loads(args[0])
        except (IndexError, TypeError):
            return 'API methods require a single JSON encoded dictionary as input. For example: input = json.dumps({\'param_1\': 1, \'param_2\': [2, 3]})'

        odict = self._call_wrapped(method, idict)

        return json.dumps(odict)

    def _call_wrapped(self, method, idict):
        odict = {}

        try:
            profile = cProfile.Profile()
            profile.enable()
            data = method(idict)
            profile.disable()
            stream = cStringIO.StringIO()
            stats = pstats.Stats(profile, stream=stream)
            stats.strip_dirs()
            stats.sort_stats(1)
            stats.print_stats(20)
        except:
            odict['data']       = data
            odict['error']      = traceback.format_exc()
            odict['profile']    = None
        else:
            odict['data']       = data
            odict['error']      = None
            odict['profile']    = stream.getvalue()

        return odict


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
