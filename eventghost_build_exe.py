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
import os
from subprocess import Popen, PIPE
from cx_Freeze.dist import build_exe

INNO_SETUP_DEFINES = '''
#define APPNAME "{name}"
#define APPVERSION "{version}"
#define APPCOPYRIGHT "{copyright}"
#define APPPUBLISHER "{company_name}"
#define APPURL "{url}"
#define APPBUILDPATH "{build_dir}"
#define APPOUTPUTDIR "{output_dir}"
#define APPICON "{icon}"
#define APPLOGOSMALL "{logo_small}"
#define APPLOGOLARGE "{logo_large}"

'''


class BuildEXE(build_exe):

    def build_extension(self, name, **_):
        pass

    def run(self):
        command = self.distribution.get_command_obj('build_ext')
        command.run()
        #
        # self.distribution.get_command_obj('build_docs').run()
        build_exe.run(self)

        from inno_setup import COMPILER_PATH
        from docs import ICON, LOGO_SMALL, LOGO_LARGE

        build_base = os.path.split(self.build_exe)[0]
        inno_build_path = os.path.join(build_base, 'inno_setup')

        base_path = os.path.dirname(__file__)
        output_path = os.path.join(base_path, 'output')
        inno_path = os.path.join(base_path, 'inno_setup')

        copyright = self.distribution.executables[0].copyright
        metadata = self.distribution.metadata

        os.remove(os.path.join(self.build_exe, 'EventGhost.pyw'))
        os.remove(os.path.join(self.build_exe, 'Interpreter.py'))

        template = os.path.join(inno_path, 'InnoSetup.template')
        script = os.path.join(inno_build_path, 'inno_setup.iss')

        defines = INNO_SETUP_DEFINES.format(
            name=metadata.name,
            version=metadata.version,
            copyright=copyright.replace('\n', ' '),
            company_name=metadata.name + ' Project',
            url=metadata.url,
            build_dir=self.build_exe,
            output_dir=output_path,
            icon=ICON,
            logo_small=LOGO_SMALL,
            logo_large=LOGO_LARGE
        )

        with open(template, 'r', encoding='utf-8') as f:
            template = f.read()

        with open(script, 'w', encoding='utf-8') as f:
            f.write(defines)
            f.write(template)

        print('-- building installer ' + '-' * 58)

        proc = Popen(
            '"{0}" "{1}"'.format(COMPILER_PATH, script),
            stdout=PIPE,
            stderr=PIPE
        )

        if sys.version_info[0] >= 3:
            empty_return = b''
        else:
            empty_return = ''

        while proc.poll() is None:
            for line in iter(proc.stdout.readline, empty_return):
                if line:
                    print(line.rstrip().decode('utf-8'))
