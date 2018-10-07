# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

"""
Builds a file that would import all used modules.

This way we trick py2exe to include all standard library files and some more
packages and modules.
"""

import os
import sys
import warnings

MODULES_TO_IGNORE = [
    "__phello__.foo",
    "antigravity",
    "unittest",
    "win32com.propsys.propsys",
    "wx.lib.graphics",
    "wx.lib.rpcMixin",
    "wx.lib.wxcairo",
    "wx.build.config",
    'plat-aix4',
    'plat-darwin',
    'plat-freebsd4',
    'plat-freebsd5',
    'plat-freebsd6',
    'plat-freebsd7',
    'plat-freebsd8',
    'plat-generic',
    'plat-linux',
    'plat-netbsd1',
    'plat-next3',
    'plat-sunos5',
    'plat-unixware7',
    'site-packages',
    'collections.__main__',
    '_osx_support',
    'macpath',
    'lzma',
    'this',
    'macurl2path',
    'venv',
    'lib2to3.__main__'
]
PACKAGES = [
    'requests',
    'agithub',
    'pycurl',
    'qrcode',
    'tornado',
    'psutil',
    'CommonMark',
    'comtypes',
    'future',
    'PIL',
    'crypto',
    'wx',
    'websocket',
    'docutils',
    'winsound',
    'difflib',
]

INCLUDES = [
    'pywin32',
    'mmapfile',
    'odbc',
    'perfmon',
    'servicemanager',
    'timer',
    'win2kras',
    'win32api',
    'win32clipboard',
    'win32console',
    'win32cred',
    'win32crypt',
    'win32event',
    'win32evtlog',
    'win32file',
    'win32gui',
    'win32help',
    'win32inet',
    'win32job',
    'win32lz',
    'win32net',
    'win32pdh',
    'win32pipe',
    'win32print',
    'win32process',
    'win32profile',
    'win32ras',
    'win32security',
    'win32service',
    'win32trace',
    'win32transaction',
    'win32ts',
    'win32wnet',
    'winxpgui',
    '_win32sysloader',
    '_winxptheme',
    'win32com.storagecon',
    'win32com.universal',
    'win32com.util',
    'win32com.olectl',
    'win32com.server',
    'win32com.servers',
    'win32com.bits',
    'win32com.bits',
    'win32com.directsound',
    'win32com.ifilter',
    'win32com.internet',
    'win32com.mapi',
    'win32com.propsys',
    'win32com.shell',
    'win32com.taskscheduler',
]

EXCLUDES = [
    '_imagingtk',
    '_tkinter',
    'cffi',
    'comtypes.gen',
    'curses',
    'distutils.command.bdist_packager',
    'distutils.mwerkscompiler',
    'FixTk',
    'gopherlib',
    'idlelib',
    'ImageGL',
    'ImageQt',
    'ImageTk',
    'ipaddr',
    'ipaddress',
    'lib2to3',
    'PIL._imagingtk',
    'PIL.ImageTk',
    'pyasn1',
    'pycparser',
    'pywin',
    'simplejson',
    'tcl',
    'test',
    'Tix',
    'Tkconstants',
    'tkinter',
    'Tkinter',
    'turtle',
    'WalImageFile',
    'win32com.axdebug',
    'win32com.axscript',
    'win32com.demos',
    'win32com.gen_py',
    'sqlite3',
    'doctest',
    'unittest',
    'pydoc',
    'pygments',
    'pdb',
    'difflib',
    'numpy',
    'dbi',
    'regcheck',
    'win32traceutil',
    'py2exe'
]

PY_PATH = sys.real_prefix if hasattr(sys, "real_prefix") else sys.prefix
MODULES_TO_IGNORE += EXCLUDES[:]

HEADER = """\
# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

#-----------------------------------------------------------------------------
# This file was automatically created by the BuildImports.py script.
# Don't try to edit this file yourself.
#-----------------------------------------------------------------------------
#pylint: disable-msg=W0611,W0622,W0402,E0611,F0401
"""


def test_import(module):
    if module in MODULES_TO_IGNORE or 'test' in module:
        return None
    try:
        mod = __import__(module)
        return mod
    except:
        pass


def find_modules(path, module=""):
    """
    Find modules and packages for a given filesystem path.
    """
    modules = []

    if module in MODULES_TO_IGNORE:
        return []

    if module:
        module += "."

    dirs = []
    try:
        files = os.listdir(path)
    except OSError:
        return modules

    if 'site-packages' in files:
        files.remove('site-packages')

    if '__init__.py' in files:
        files.remove('__init__.py')

        mod = module[:-1]
        if test_import(mod):
            modules += [mod]

    if '__pycache__' in files:
        files.remove('__pycache__')

    for file in files:
        if file in ('Demos', 'demos', 'test', 'Test'):
            continue
        if os.path.isdir(os.path.join(path, file)):
            dirs += [os.path.join(path, file)]
            continue

        if file.endswith('.py') or file.endswith('.pyd'):
            if module == 'pywin32.':
                mod = file.replace('.py', '').replace('.pyd', '')
            else:
                mod = module + file.replace('.py', '').replace('.pyd', '')
            if test_import(mod):
                modules += [mod]

    for mod_path in dirs:
        if module == 'pywin32.':
            mod = module[:-1]
        else:
            mod = module + os.path.split(mod_path)[1]

        modules += find_modules(mod_path, mod)

    return modules


def find_package_modules(package):
    modules = []
    tail = os.path.join("Lib", "site-packages", package) + ".pth"
    pths = [os.path.join(sys.prefix, tail)]

    if hasattr(sys, "real_prefix"):
        pths += [os.path.join(sys.real_prefix, tail)]
    for pth in pths:
        if os.path.exists(pth):
            for path in read_pth_file(pth):
                modules += find_modules(path, package)
            break
    else:
        mod = test_import(package)
        if mod is not None:
            if mod.__file__.endswith(".pyd"):
                return modules
            modules += find_modules(os.path.dirname(mod.__file__), package)

    return modules


def read_pth_file(path):
    with open(path, "rt") as f:
        for line in f.readlines():
            if line.strip().startswith("#"):
                continue
            yield os.path.join(os.path.dirname(path), line.strip())


# warnings.simplefilter('error', DeprecationWarning)
# OUT_FILE = os.path.join(BUILD_PATH, 'module_imports.py')

class Build(object):

    @property
    def STD_LIB_MODULES(self):
        return (
            find_modules(os.path.join(PY_PATH, "DLLs"), "") +
            find_modules(os.path.join(PY_PATH, "Lib"), "")
        )

    @property
    def INCLUDES(self):
        res = set()
        for package in INCLUDES[:]:
            for item in find_package_modules(package):
                res.add(item)

        for item in INCLUDES[1:]:
            res.add(item)
        res = list(item for item in res)
        return res

build = Build()
