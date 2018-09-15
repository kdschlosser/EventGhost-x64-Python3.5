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


class InnoSetupError(Exception):
    pass


class InnoSetupMissing(InnoSetupError):
    pass


try:
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        (
            "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\"
            "Uninstall\\Inno Setup 5_is1"
        )
    )
    try:
        COMPILER_PATH = winreg.QueryValueEx(key, "InstallLocation")[0]
        COMPILER_PATH = os.path.join(COMPILER_PATH, "ISCC.exe")
        if not os.path.exists(COMPILER_PATH):
            raise WindowsError
    finally:
        winreg.CloseKey(key)

except WindowsError:
    raise InnoSetupMissing(
        'InnoSetup Unicode >= 5.5.8 is required to build EventGhost'
    )
