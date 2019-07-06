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

from distutils.command import build_ext as _build_ext


class BuildEXT(_build_ext.build_ext):

    def get_export_symbols(self, ext):
        if ext.name in (
            'RawInputHook',
            'MceIr',
            'TaskHook',
            'WinUsbWrapper'
        ):
            return ext.export_symbols

        return _build_ext.build_ext.get_export_symbols(self, ext)

    def get_ext_filename(self, ext_name):
        if ext_name in (
            'RawInputHook',
            'MceIr',
            'TaskHook',
            'WinUsbWrapper'
        ):
            return ext_name + '.dll'

        return _build_ext.build_ext.get_ext_filename(self, ext_name)
