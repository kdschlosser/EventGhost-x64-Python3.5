import os
import sys

BASE_PATH = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(BASE_PATH, '..', '..'))

import msvc
from distutils.core import setup
from distutils.extension import Extension

print(msvc.environment)

setup(
    name='_dxJoystick',
    version='1.0',
    ext_modules=[
        Extension(
            '_dxJoystick',
            sources=['_dxJoystick.cpp'],
            include_dirs=msvc.environment.python.includes,
            library_dirs=msvc.environment.windows_sdk.lib,
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
                ('_WINDOWS', 1)
            ],
            libraries=[
                'dinput8',
                'dxguid',
                'odbc32',
                'odbccp32',
            ],
        )
    ],
)
