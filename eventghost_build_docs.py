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

from distutils.core import Command
import re
import os
import sys
import sphinx
from subprocess import Popen, PIPE


GUI_CLASSES = [
    "SpinIntCtrl",
    "SpinNumCtrl",
    "MessageDialog",
    "DisplayChoice",
    "SerialPortChoice",
    "FileBrowseButton",
    "DirBrowseButton",
    "FontSelectButton",
]

MAIN_CLASSES = [
    "PluginBase",
    "ActionBase",
    "SerialThread",
    "ThreadWorker",
    "ConfigPanel",
    "Bunch",
    "WindowMatcher",
    "WindowsVersion",
    "-EventGhostEvent",
    "-Scheduler",
    "-ControlProviderMixin",
]


def cls_docs(cls_names, doc_src_dir):
    import eg

    res = []
    for cls_name in cls_names:
        if cls_name.startswith("-"):
            cls_name = cls_name[1:]
            add_cls = False
        else:
            add_cls = True
        full_cls_name = "eg." + cls_name
        cls = getattr(eg, cls_name)

        if add_cls:
            res.append("\nclass :class:`%s`" % full_cls_name)
            if cls.__doc__:
                res.append("   %s" % get_first_paragraph(cls.__doc__))

        file_path = os.path.join(doc_src_dir, "eg", "%s.rst" % full_cls_name)
        outfile = open(file_path, "wt", encoding='utf-8')
        outfile.write(".. This file is automatically created. Don't edit it!")
        outfile.write("\n\n")
        outfile.write("=" * len(full_cls_name) + "\n")
        outfile.write(full_cls_name + "\n")
        outfile.write("=" * len(full_cls_name) + "\n")
        outfile.write("\n")
        outfile.write(".. currentmodule:: eg\n")
        outfile.write(".. autoclass:: %s\n" % full_cls_name)
        outfile.write("   :members:\n")
        if hasattr(cls, "__docsort__"):
            outfile.write("      " + cls.__docsort__)
        outfile.write("\n")
    return "\n".join(res)


def get_first_paragraph(text):
    res = []
    for line in text.lstrip().splitlines():
        if not line.strip():
            break
        res.append(line.strip())
        if line.endswith('\n'):
            break
    return " ".join(res)


class BuildDocs(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from docs import COMPILER_PATH
        from setup import (
            VERSION,
            EG_BUILD_PATH,
            HELP_DOCS_PATH,
            DOCS_BUILD_PATH
        )

        cmh_help_file = os.path.join(HELP_DOCS_PATH, "EventGhost.chm")
        hhp_help_file = os.path.join(HELP_DOCS_PATH, "EventGhost.hhp")
        plugin_list_file = os.path.join(DOCS_BUILD_PATH, "pluginlist.rst")
        sys.path.insert(0, EG_BUILD_PATH)

        print('-- building help docs ' + '-' * 58)
        import eg

        kinds = [
            ("core", "Essential (always loaded)"),
            ("remote", "Remote Receiver"),
            ("program", "Program Control"),
            ("external", "External Hardware Equipment"),
            ("other", "Other"),
        ]
        count = 0
        groups = {}
        for info in eg.pluginManager.GetPluginInfoList():
            if os.path.exists(os.path.join(info.path, "noinclude")):
                continue
            if info.kind in groups:
                groups[info.kind].append(info)
            else:
                groups[info.kind] = [info]
            count += 1

        outfile = open(plugin_list_file, "w", encoding="utf-8")
        outfile.write(
            ".. This file is automatically created. Don't edit it!\n\n")
        outfile.write(".. _pluginlist:\n\n")
        outfile.write("List of Plugins\n")
        outfile.write("===============\n\n")
        outfile.write("This is the list of the %d plugins " % count)
        outfile.write("currently distributed with EventGhost ")
        outfile.write("%s:\n\n" % eg.Version.base)

        for kind, kind_description in kinds:
            outfile.write("%s\n" % kind_description)
            outfile.write(len(kind_description) * "-" + "\n\n")
            groups[kind].sort(key=lambda x: x.name)
            for info in groups[kind]:
                description = get_first_paragraph(info.description)
                description = re.sub(
                    r'<a\s+.*?href=["\']http://(.*?)["\']>\s*((\n|.)+?)\s*</a>',
                    r'`\2 <http://\1>`_',
                    description
                )
                if info.url:
                    outfile.write("|%s Plugin|_\n" % info.name)
                else:
                    outfile.write("**%s**\n" % info.name)
                outfile.write(u"   %s\n\n" % description)
                if info.url:
                    outfile.write(
                        ".. |%s Plugin| replace:: **%s**\n" %
                        (info.name, info.name)
                    )
                    outfile.write(
                        ".. _%s Plugin: %s\n\n" %
                        (info.name, info.url)
                    )
        outfile.write('\n')
        outfile.close()

        file_path = os.path.join(DOCS_BUILD_PATH, "eg", "classes.txt")
        outfile = open(file_path, "wt", encoding='utf-8')
        outfile.write(cls_docs(MAIN_CLASSES, DOCS_BUILD_PATH) + '\n')
        outfile.close()

        file_path = os.path.join(DOCS_BUILD_PATH, "eg", "gui_classes.txt")
        outfile = open(file_path, "wt", encoding='utf-8')
        outfile.write(cls_docs(GUI_CLASSES, DOCS_BUILD_PATH) + '\n')
        outfile.close()

        sphinx.build_main(
            [
                None,
                "-D", "project=EventGhost",
                "-D", "copyright=2005-2017 EventGhost Project",
                # "-D", "templates_path=[]",
                '-q',  # be quiet
                # "-a",  # always write all output files
                # "-E",  # Don’t use a saved environment (the structure
                # caching all cross-references),
                # "-N",  # Prevent colored output.
                # "-P",  # (Useful for debugging only.) Run the Python debugger,
                # pdb, if an unhandled exception occurs while building.
                # '-v',  # verbosity, can be given up to three times
                # '-v',
                # write warnings and errors to file:
                # '-w', join('output', 'sphinx_log_chm.txt'),
                "-b", 'htmlhelp',
                "-D", "version=%s" % VERSION,
                "-D", "release=%s" % VERSION,
                "-d", os.path.join(DOCS_BUILD_PATH, ".doctree"),
                DOCS_BUILD_PATH,
                HELP_DOCS_PATH,
            ]
        )

        proc = Popen(
            '"{0}" "{1}"'.format(COMPILER_PATH, hhp_help_file),
            stdout=PIPE,
            stderr=PIPE
        )

        while proc.poll() is None:
            if sys.version_info[0] >= 3:
                empty_return = b''
            else:
                empty_return = ''
            for line in iter(proc.stdout.readline, empty_return):
                if line:
                    sys.stdout.write(line.decode('utf-8'))

        self.copy_file(cmh_help_file, EG_BUILD_PATH)
