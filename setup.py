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

import msvc
import os
import sys
import shutil
import site
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

try:
    import setuptools
except ImportError:
    raise RuntimeError(
        'The setuptools module is needed to build EventGhost '
        '(python -m pip install setuptools)'
    )
print('Checking if any modules need to be installed.')
print('This may take a bit so be patient....')
setuptools.setup(
    script_args=['install'],
    name='EventGhost module dependencies',
    setup_requires=[
        'cx_Freeze>=5.1.1',
        'requests>=2.19.1',
        'agithub>=2.1',
        'qrcode>=6.0',
        'tornado>=5.1',
        'psutil>=5.4.7',
        'websocket-client-py3>=0.15.0',
        'CommonMark>=0.7.5',
        'comtypes>=1.1.7',
        'future>=0.16.0',
        'Pillow>=5.2.0',
        'PyCrypto>=2.6.1',
        'Sphinx>=1.8.0b1',
        'wxPython>=4.0.3',
        'pywin32>=223',
        'pycurl==7.43.0.2'
    ],
    dependency_links=[
        'https://files.pythonhosted.org/packages/41/67/5b85efde1641b71446c'
        '2bdea194be860c5cea4efc42b4f69933213ec69f4/pycurl-7.43.0.2-cp35-cp'
        '35m-win_amd64.whl'
    ],
)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
EGG_PATH = os.path.join(BASE_PATH, '.eggs')

if os.path.exists(EGG_PATH):
    pth_data = ''

    for f in os.listdir(EGG_PATH):
        mod = os.path.join(EGG_PATH, f)
        if os.path.isdir(mod):
            has_pth = list('pth' for p in os.listdir(mod) if p.endswith('pth'))
            if has_pth:
                site.addsitedir(mod)
            else:
                pth_data += './' + f + '\n'

    with open(os.path.join(EGG_PATH, 'modules.pth'), 'w') as f:
        f.write(pth_data)

    site.addsitedir(EGG_PATH)

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


PY_VERSION = "%d%d" % sys.version_info[:2]
PY_BASE_NAME = "py%s" % PY_VERSION
PYW_BASE_NAME = "pyw%s" % PY_VERSION

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
RAW_INPUT_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'RawInputHook.dll')
MCE_IR_SRC = os.path.join(EXTENSIONS_PATH, 'MceIr.dll')
TASK_HOOK_SRC = os.path.join(EXTENSIONS_PATH, 'TaskHook.dll')
C_FUNCTIONS_SRC = os.path.join(EXTENSIONS_PATH, 'cFunctions')
DX_JOYSTICK_SRC = os.path.join(EXTENSIONS_PATH, '_dxJoystick')
VISTA_VOL_EVENTS_SRC = os.path.join(EXTENSIONS_PATH, 'VistaVolEvents')
WIN_USB_SRC = os.path.join(EXTENSIONS_PATH, 'WinUsbWrapper')

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
    DOCS_BUILD_PATH
):
    os.mkdir(path)

import eventghost_build_logging # NOQA
sys.stdout = eventghost_build_logging.STD(sys.stdout, 'INFO')
sys.stderr = eventghost_build_logging.STD(sys.stderr, 'ERROR')

iter_copy(SOURCE_PATH, EG_BUILD_PATH)
iter_copy(DOCS_PATH, DOCS_BUILD_PATH)

import cx_Freeze # NOQA
import includes # NOQA
import eventghost_build_ext # NOQA
import eventghost_build_exe # NOQA
import eventghost_build # NOQA
import eventghost_build_docs # NOQA


RawInputHook = setuptools.Extension(
    'RawInputHook',
    sources=[
        os.path.join(RAW_INPUT_HOOK_SRC, 'RawInputHook.cpp'),
        os.path.join(RAW_INPUT_HOOK_SRC, 'stdafx.cpp'),
    ],
    include_dirs=[RAW_INPUT_HOOK_SRC],
    library_dirs=msvc.environment.windows_sdk.lib,
    extra_link_args=[
        '/def:"' + os.path.join(RAW_INPUT_HOOK_SRC, 'RawInputHook.def') + '"'
    ],
    extra_compile_args=[
        # Enables function-level linking.
        '/Gy',
        # Creates fast code.
        '/O2',
        # Uses the __cdecl calling convention (x86 only).
        '/Gd',
        # Omits frame pointer (x86 only).
        '/Oy',
        # Generates intrinsic functions.
        '/Oi',
        # Specify floating-point behavior.
        '/fp:precise',
        # Specifies standard behavior
        '/Zc:wchar_t',
        # Specifies standard behavior
        '/Zc:forScope',
        # I cannot remember what this does. I do know it does get rid of
        # a compiler warning
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1),
        ('_USRDLL', 1),
        ('HOOK_EXPORTS', 1)
    ],
    libraries=['user32']
)

MceIr = setuptools.Extension(
    'MceIr',
    sources=[
        os.path.join(MCE_IR_SRC, 'IrDec.cpp'),
        os.path.join(MCE_IR_SRC, 'MceIr.cpp'),
        os.path.join(MCE_IR_SRC, 'StdAfx.cpp'),
    ],
    include_dirs=[MCE_IR_SRC],
    library_dirs=msvc.environment.windows_sdk.lib,
    extra_link_args=[
        '/def:"' + os.path.join(MCE_IR_SRC, 'MceIr.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1),
        ('_USRDLL', 1),
        ('MCEIR_EXPORTS', 1)
    ],
    libraries=['setupapi', 'user32']
)


TaskHook = setuptools.Extension(
    'TaskHook',
    sources=[
        os.path.join(TASK_HOOK_SRC, 'hook.cpp'),
        os.path.join(TASK_HOOK_SRC, 'stdafx.cpp'),
    ],
    include_dirs=[TASK_HOOK_SRC],
    library_dirs=msvc.environment.windows_sdk.lib,
    extra_link_args=[
        '/def:"' + os.path.join(TASK_HOOK_SRC, 'hook.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1),
        ('_USRDLL', 1),
        ('HOOK_EXPORTS', 1)
    ],
    libraries=['user32']
)


lib_path = msvc.environment.windows_sdk.lib[0]
lib_path = lib_path.replace('ucrt', 'km').replace('um', 'km')

WinUsbWrapper = setuptools.Extension(
    'WinUsbWrapper',
    sources=[
        os.path.join(WIN_USB_SRC, 'dllmain.cpp'),
        os.path.join(WIN_USB_SRC, 'stdafx.cpp'),
    ],
    include_dirs=[WIN_USB_SRC],
    library_dirs=[lib_path] + msvc.environment.windows_sdk.lib,
    extra_link_args=[
        '/def:"' + os.path.join(WIN_USB_SRC, 'dllmain.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1),
        ('_USRDLL', 1),
        ('WINUSBWRAPPER_EXPORTS', 1)
    ],
    libraries=['kernel32', 'user32', 'ole32', 'setupapi', 'winusb']
)

cFunctions = setuptools.Extension(
    'cFunctions',
    sources=[
        os.path.join(C_FUNCTIONS_SRC, 'hooks.c'),
        os.path.join(C_FUNCTIONS_SRC, 'keyhook.c'),
        os.path.join(C_FUNCTIONS_SRC, 'main.c'),
        os.path.join(C_FUNCTIONS_SRC, 'mousehook.c'),
        os.path.join(C_FUNCTIONS_SRC, 'registry_funcs.c'),
        os.path.join(C_FUNCTIONS_SRC, 'utils.c'),
        os.path.join(C_FUNCTIONS_SRC, 'win_funcs.c')
    ],
    include_dirs=[C_FUNCTIONS_SRC] + msvc.environment.python.includes,
    library_dirs=(
        msvc.environment.windows_sdk.lib +
        msvc.environment.python.libraries
    ),
    extra_link_args=[
        '/def:"' + os.path.join(C_FUNCTIONS_SRC, 'main.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1)
    ],
    libraries=[
        'user32',
        'advapi32',
        'ole32',
        msvc.environment.python.dependency[:-4]
    ]
)


_dxJoystick = setuptools.Extension(
    '_dxJoystick',
    sources=[os.path.join(DX_JOYSTICK_SRC, '_dxJoystick.cpp')],
    include_dirs=msvc.environment.python.includes,
    library_dirs=msvc.environment.windows_sdk.lib,
    extra_link_args=[
        '/def:"' + os.path.join(DX_JOYSTICK_SRC, '_dxJoystick.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1)
    ],
    libraries=[
        'dinput8',
        'dxguid',
        'odbc32',
        'odbccp32',
    ]
)

VistaVolEvents = setuptools.Extension(
    'VistaVolEvents',
    sources=[
        os.path.join(VISTA_VOL_EVENTS_SRC, 'dllmain.cpp'),
        os.path.join(VISTA_VOL_EVENTS_SRC, 'stdafx.cpp'),
        os.path.join(VISTA_VOL_EVENTS_SRC, 'VistaVolume.cpp')
    ],
    include_dirs=[VISTA_VOL_EVENTS_SRC] + msvc.environment.python.includes,
    library_dirs=(
        msvc.environment.windows_sdk.lib +
        msvc.environment.python.libraries
    ),
    extra_link_args=[
        '/def:"' + os.path.join(VISTA_VOL_EVENTS_SRC, 'dllmain.def') + '"'
    ],
    extra_compile_args=[
        '/Gy',
        '/O2',
        '/Gd',
        '/Oy',
        '/Oi',
        '/fp:precise',
        '/Zc:wchar_t',
        '/Zc:forScope',
        '/EHsc',
    ],
    define_macros=[
        ('WIN64', 1),
        ('NDEBUG', 1),
        ('_WINDOWS', 1),
        ('_USRDLL', 1),
        ('VISTAVOLEVENTS_EXPORTS', 1),
    ],
    libraries=[
        'kernel32',
        'user32',
        'gdi32',
        'winspool',
        'comdlg32',
        'advapi32',
        'shell32',
        'ole32',
        'oleaut32',
        'uuid',
        'odbc32',
        'odbccp32',
        msvc.environment.python.dependency[:-4]
    ]
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
        WinUsbWrapper,
        RawInputHook,
        MceIr,
        TaskHook,
        cFunctions,
        _dxJoystick,
        VistaVolEvents
    ]
)


print('\n\n-- FINISHED ------------------------------------------------------')


