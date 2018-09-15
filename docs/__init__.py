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


import os
import winreg


class HTMLHelpError(Exception):
    pass


class HTMLHelpMissing(HTMLHelpError):
    pass


subkey = r"Software\Microsoft\HTML Help Workshop"
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey)
    try:
        COMPILER_PATH = winreg.QueryValueEx(key, "InstallDir")[0]
    finally:
        winreg.CloseKey(key)
except WindowsError:
    COMPILER_PATH = os.path.join(
        os.environ["PROGRAMFILES"],
        "HTML Help Workshop"
    )

COMPILER_PATH = os.path.join(COMPILER_PATH, "hhc.exe")

if not os.path.exists(COMPILER_PATH):
    raise HTMLHelpMissing(
        'Microsoft HTML Help Compiler is required to build EventGhost'
    )

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
ICON = os.path.join(BASE_PATH, "_static", "logo.ico")
LOGO_LARGE = os.path.join(BASE_PATH, "_static", "logo.bmp")
LOGO_SMALL = os.path.join(BASE_PATH, "_static", "logo_small.bmp")
