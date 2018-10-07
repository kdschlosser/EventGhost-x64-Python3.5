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
import sys
from os.path import exists, join

# Local imports
import eg

class PluginModuleInfo(object):
    """
    Holds information of a plugin module.

    The main purpose of this class is to get the information from the
    eg.RegisterPlugin call inside the plugin module. So it imports the main
    module, but stops the import immediately after the eg.RegisterPlugin call.
    """
    name = "Unknown Plugin"
    description = ""
    author = "[unknown author]"
    version = "[unknown version]"
    kind = "other"
    guid = ""
    canMultiLoad = False
    createMacrosOnAdd = False
    icon = eg.Icons.PLUGIN_ICON
    url = None
    englishName = None
    englishDescription = None
    path = None
    pluginName = None
    hardwareId = ""
    valid = False

    def __init__(self, path):
        self.description = self.path = path
        self.name = self.pluginName = os.path.basename(path)

        originalRegisterPlugin = eg.RegisterPlugin
        eg.RegisterPlugin = self.RegisterPlugin

        if self.path.startswith(eg.corePluginDir):
            self.RegisterPluginException = (
                eg.CorePluginModule.RegisterPluginException
            )
            self.valid = getattr(eg.CorePluginModule, self.pluginName)
        else:
            self.RegisterPluginException = (
                eg.UserPluginModule.RegisterPluginException
            )

            self.valid = getattr(eg.UserPluginModule, self.pluginName)

        eg.RegisterPlugin = originalRegisterPlugin

    if eg.debugLevel:
        def __setattr__(self, name, value):
            if not hasattr(self.__class__, name):
                raise AttributeError(
                    "%s has no attribute %s" % (self.__class__.__name__, name)
                )
            object.__setattr__(self, name, value)

    def RegisterPlugin(
        self,
        name = None,
        description = None,
        kind = "other",
        author = "[unknown author]",
        version = "[unknown version]",
        icon = None,
        canMultiLoad = False,
        createMacrosOnAdd = False,
        url = None,
        help = None,
        guid = "",
        hardwareId = "",
        **kwargs
    ):
        if name is None:
            name = self.pluginName
        if description is None:
            description = name
        if help is not None:
            help = "\n".join([s.strip() for s in help.splitlines()])
            help = help.replace("\n\n", "<p>")
            description += "\n\n<p>" + help
        self.name = self.englishName = unicode(name)
        self.description = self.englishDescription = unicode(description)
        self.kind = unicode(kind)
        self.author = (
            unicode(", ".join(author)) if isinstance(author, tuple)
            else unicode(author)
        )
        self.version = unicode(version)
        self.canMultiLoad = canMultiLoad
        self.createMacrosOnAdd = createMacrosOnAdd
        self.url = unicode(url) if url else url  # Added by Pako
        self.guid = guid.upper()
        if not guid:
            eg.PrintDebugNotice("missing guid in plugin: %s" % self.path)
            self.guid = self.pluginName
        self.hardwareId = hardwareId.upper()
        # get the icon if any
        if icon is not None:
            self.icon = eg.Icons.StringIcon(icon)
        else:
            iconPath = join(self.path, "icon.png")
            if exists(iconPath):
                self.icon = eg.Icons.PathIcon(iconPath)

        # try to translate name and description
        textCls = getattr(eg.text.Plugin, self.pluginName, None)
        if textCls is not None:
            self.name = getattr(textCls, "name", name)
            self.description = getattr(textCls, "description", description)

        # we are done with this plugin module, so we can interrupt further
        # processing by raising RegisterPluginException
        raise self.RegisterPluginException

