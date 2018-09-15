# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import sys
import builtins
import winreg
import pickle
from io import StringIO as _StringIO
import http.server
import http.client
import socketserver
import urllib.parse
import urllib.request
import urllib.error
import urllib.response
import types
import ctypes.wintypes
import ctypes


ctypes.wintypes.GetLastError = ctypes.GetLastError

types.ClassType = type
types.UnicodeType = str
types.InstanceType = object

_urllib_parse = urllib.parse
_urllib_request = urllib.request
_urllib_error = urllib.error
_urllib_response = urllib.response
sys.maxint = sys.maxsize
builtins.unicode = str
builtins.xrange = range
_import = builtins.__import__


class URLLib2(object):
    MAXFTPCACHE = 10
    toBytes = _urllib_parse.unquote_to_bytes
    always_safe = _urllib_parse._ALWAYS_SAFE
    randombytes = _urllib_request._randombytes

    def __getattr__(self, item):
        for mod in (
            _urllib_parse,
            _urllib_request,
            _urllib_error,
            _urllib_response
        ):
            if hasattr(mod, item):
                return getattr(mod, item)

        raise AttributeError(item)

    @staticmethod
    def splitnport(host, defport=-1):
        import re

        nportprog = re.compile('^(.*):(.*)$')
        match = nportprog.match(host)
        if match:
            host, port = match.group(1, 2)
            if port:
                try:
                    nport = int(port)
                except ValueError:
                    nport = None
                return host, nport
        return host, defport


class cStringIO(object):
    __name__ = 'cStringIO'
    __package__ = ''

    StringIO = _StringIO


class StringIO(object):
    __name__ = 'StringIO'
    __package__ = ''

    StringIO = _StringIO


def import_(name, globals=None, locals=None, fromlist=(), level=0):
    try:
        return _import(name, globals, locals, fromlist, level)
    except ImportError:
        return _import(name, globals, locals, fromlist, 1)


urllib2 = URLLib2()

builtins.__import__ = import_
sys.modules['__builtin__'] = builtins
sys.modules["cStringIO"] = cStringIO
sys.modules["StringIO"] = StringIO
sys.modules['_winreg'] = winreg
sys.modules['cPickle'] = pickle
sys.modules['SimpleHTTPServer'] = http.server
sys.modules['BaseHTTPServer'] = http.server
sys.modules['SocketServer'] = socketserver
sys.modules['httplib'] = http.client
sys.modules['urllib2'] = urllib2
sys.modules['urllib'] = urllib2
sys.modules['types'] = types
sys.modules['ctypes.wintypes'] = ctypes.wintypes

from . import wxPython3to4
