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

import os
import sys
import shutil
from pkg_resources import parse_version

try:
    import stackless  # NOQA
    if (
        parse_version("%d.%d.%d" % sys.version_info[:3]) <
        parse_version('3.5.0')
    ):
        raise ImportError

except ImportError:
    raise RuntimeError(
        'Stackless Python >= 3.5.0 is required to build EventGhost'
    )

__import__('inno_setup')
__import__('docs')

NAME = 'EventGhost'
DESCRIPTION = 'EventGhost Automation Tool'
VERSION = '1.0.0'
COMPANY_NAME = 'EventGhost Project'
URL = 'https://www.eventghost.net'
AUTHOR = 'Many'
PROJECT_NAME = 'EventGhost'
COPYRIGHT = (
    'Copyright © 2005-2018 EventGhost Project\n'
    '<http://www.eventghost.net/>'
)

REQUIRES = [
    'cx_Freeze >= 5.1.1',
    'requests >= 2.19.1',
    'agithub >= 2.1',
    'pycurl >= 1.43.0.2',
    'qrcode >= 6.0',
    'tornado >= 5.1',
    'psutil >= 5.4.7',
    'websocket-client-py3 >= 0.15.0',
    'CommonMark >= 0.7.5',
    'comtypes >= 1.1.7',
    'future >= 0.16.0',
    'Pillow >= 5.2.0',
    'PyCrypto >= 2.6.1',
    'Sphinx >= 1.8.0b1',
    'wxPython >= 4.0.3',
    'pywin32 >= 223',
    'setuptools >= 40.2'
]

PY_VERSION = "%d%d" % sys.version_info[:2]
PY_BASE_NAME = "py%s" % PY_VERSION
PYW_BASE_NAME = "pyw%s" % PY_VERSION


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
SOURCE_PATH = os.path.join(BASE_PATH, 'EventGhost')
BUILD_PATH = os.path.join(BASE_PATH, 'build')
EG_BUILD_PATH = os.path.join(BUILD_PATH, 'eventghost')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
HELP_DOCS_PATH = os.path.join(BUILD_PATH, 'chm')

DOCS_PATH = os.path.join(BASE_PATH, 'docs')
DOCS_BUILD_PATH = os.path.join(BUILD_PATH, 'docs')
INNO_PATH = os.path.join(BASE_PATH, 'inno_setup')
INNO_BUILD_PATH = os.path.join(BUILD_PATH, 'inno_setup')
INIT_SCRIPT = os.path.join(BASE_PATH, 'init_scripts', 'init_script.py')

EXTENSIONS_PATH = os.path.join(BASE_PATH, 'extensions')
EXTENSIONS_BUILD_PATH = os.path.join(BUILD_PATH, 'extensions')
PYD_IMPORTS_PATH = os.path.join(EXTENSIONS_BUILD_PATH, 'pyd_imports')
PLUGINS_PATH = os.path.join(EG_BUILD_PATH, 'plugins')

RAW_INPUT_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'RawInputHook.dll')
RAW_INPUT_HOOK_DST = os.path.join(PLUGINS_PATH, 'RawInput')

MCE_IR_SRC = os.path.join(EXTENSIONS_PATH, 'MceIr.dll')
MCE_IR_DST = os.path.join(PLUGINS_PATH, 'MceRemote')

TASK_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'TaskHook.dll')
TASK_HOOK_DST = os.path.join(PLUGINS_PATH, 'Task')

C_FUNCTIONS_SRC = os.path.join(EXTENSIONS_PATH, 'cFunctions')
C_FUNCTIONS_DST = PYD_IMPORTS_PATH

DX_JOYSTICK_SRC = os.path.join(EXTENSIONS_PATH, '_dxJoystick')
DX_JOYSTICK_DST = PYD_IMPORTS_PATH

VISTA_VOL_EVENTS_SRC = os.path.join(EXTENSIONS_PATH, 'VistaVolEvents')
VISTA_VOL_EVENTS_DST = PYD_IMPORTS_PATH

WIN_USB_SRC = os.path.join(EXTENSIONS_PATH, 'WinUsbWrapper')
WIN_USB_DST = os.path.join(EG_BUILD_PATH, 'eg', 'WinApi')

import docs # NOQA

ICON = docs.ICON
LOGO_SMALL = docs.LOGO_SMALL
LOGO_LARGE = docs.LOGO_LARGE


def iter_copy(src, dst):
    if '__pycache__' in src:
        return
    if not os.path.exists(dst):
        os.mkdir(dst)

    for f in os.listdir(src):
        if os.path.isdir(os.path.join(src, f)):
            iter_copy(os.path.join(src, f), os.path.join(dst, f))
        else:
            print(
                'Copying... {0} --> {1}'.format(
                    os.path.relpath(os.path.join(src, f)),
                    os.path.relpath(os.path.join(dst, f))
                )
            )
            with open(os.path.join(src, f), 'rb') as src_file:
                with open(os.path.join(dst, f), 'wb') as dst_file:
                    dst_file.write(src_file.read())


if os.path.exists(BUILD_PATH):
    shutil.rmtree(BUILD_PATH, True)

if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH, True)

for path in (
    BUILD_PATH,
    OUTPUT_PATH,
    EG_BUILD_PATH,
    HELP_DOCS_PATH,
    INNO_BUILD_PATH,
    EXTENSIONS_BUILD_PATH,
    PYD_IMPORTS_PATH,
    DOCS_BUILD_PATH
):
    os.mkdir(path)

iter_copy(SOURCE_PATH, EG_BUILD_PATH)
iter_copy(DOCS_PATH, DOCS_BUILD_PATH)

sys.path.append(PYD_IMPORTS_PATH)

import setuptools
import cx_Freeze
import includes
import eventghost_build_ext
import eventghost_build_exe
import eventghost_build
import eventghost_build_docs


RawInputHook = eventghost_build_ext.Extension(
    'RawInputHook.dll',
    RAW_INPUT_HOOK_SRC,
    RAW_INPUT_HOOK_DST
)

MceIr = eventghost_build_ext.Extension(
    'MceIr.dll',
    MCE_IR_SRC,
    MCE_IR_DST
)

TaskHook = eventghost_build_ext.Extension(
    'TaskHook.dll',
    TASK_HOOK_SRC,
    TASK_HOOK_DST
)

cFunctions = eventghost_build_ext.Extension(
    'cFunctions.pyd',
    C_FUNCTIONS_SRC,
    C_FUNCTIONS_DST
)

_dxJoystick = eventghost_build_ext.Extension(
    '_dxJoystick.pyd',
    DX_JOYSTICK_SRC,
    DX_JOYSTICK_DST
)

VistaVolEvents = eventghost_build_ext.Extension(
    'VistaVolEvents.pyd',
    VISTA_VOL_EVENTS_SRC,
    VISTA_VOL_EVENTS_DST
)

WinUsbWrapper = eventghost_build_ext.Extension(
    'WinUsbWrapper.dll',
    WIN_USB_SRC,
    WIN_USB_DST
)

eventghost = cx_Freeze.Executable(
    script=os.path.join(EG_BUILD_PATH, 'EventGhost.pyw'),
    base="Win32GUI",
    targetName=NAME + '.exe',
    # initScript=INIT_SCRIPT,
    copyright=COPYRIGHT,
    icon=ICON,
)

pyw = cx_Freeze.Executable(
    script=os.path.join(EG_BUILD_PATH, 'Interpreter.py'),
    base="Win32GUI",
    targetName=PYW_BASE_NAME + '.exe',
    copyright=COPYRIGHT,
)

py = cx_Freeze.Executable(
    script=os.path.join(EG_BUILD_PATH, 'Interpreter.py'),
    base="Win32GUI",
    targetName=PY_BASE_NAME + '.exe',
    copyright=COPYRIGHT,
)

cx_Freeze.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    verbose=1,
    # zip_safe=False,
    setup_requires=REQUIRES,
    executables=[eventghost, pyw, py],
    options=dict(
        build=dict(
            build_exe=EG_BUILD_PATH,
        ),
        build_exe=dict(
            # build_base=EG_BUILD_PATH,
            excludes=includes.EXCLUDES,
            includes=[
                '_dxJoystick',
                'cFunctions',
                'VistaVolEvents'
            ] + includes.build.STD_LIB_MODULES + includes.build.INCLUDES,
            packages=includes.PACKAGES,
            # namespace_packages=[],
            # replace_paths=[],
            # constants=[],
            # include_files=[],
            # zip_includes=['*'],
            # bin_excludes=[],
            # bin_includes=[],
            # bin_path_includes=[],
            # bin_path_excludes=[],
            zip_include_packages=['*'],
            zip_exclude_packages=[],
            optimize=0,
            no_compress=True,
            include_msvcr=False,
            silent=False,
        )
    ),
    cmdclass=dict(
        build_exe=eventghost_build_exe.BuildEXE,
        build_ext=eventghost_build_ext.BuildEXT,
        build_docs=eventghost_build_docs.BuildDocs,
        build=eventghost_build.Build,
    ),
    ext_modules=[
        RawInputHook,
        MceIr,
        TaskHook,
        cFunctions,
        _dxJoystick,
        VistaVolEvents,
        WinUsbWrapper
    ]
)



print('\n\n-- FINISHED ------------------------------------------------------')


