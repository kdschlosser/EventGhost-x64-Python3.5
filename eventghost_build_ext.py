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
from distutils.core import Command
import sys
from subprocess import Popen, PIPE


class Extension(object):
    def __init__(self, name, solution_path, destination_path):
        self.name = name
        self.solution_path = solution_path
        self.destination_path = destination_path


class BuildEXT(Command):

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import msvc

        extensions_build_path = os.path.join(
            os.path.split(
                self.distribution.get_command_obj("build").build_exe
            )[0],
            'extensions'
        )

        extensions = self.distribution.ext_modules
        environment = msvc.Environment()

        print(environment)

        for variable, setting in environment:
            os.environ[variable] = setting

        for ext in extensions:
            name = ext.name
            solution_path = ext.solution_path
            destination_path = ext.destination_path
            build_path = os.path.join(extensions_build_path, name)

            print(
                '\n\n-- updating solution {0} {1}\n\n'.format(
                    name,
                    '-' * (59 - len(ext.name))
                )
            )

            solution, output_path = environment.update_solution(
                os.path.abspath(solution_path),
                os.path.abspath(build_path)
            )

            build_command = environment.get_build_command(solution)

            print(
                '\n\n-- building {0} {1}\n\n'.format(
                    name,
                    '-' * (68 - len(name))
                )
            )

            proc = Popen(build_command, stdout=PIPE, stderr=PIPE)

            if sys.version_info[0] >= 3:
                empty_return = b''
            else:
                empty_return = ''

            while proc.poll() is None:
                for line in iter(proc.stdout.readline, empty_return):
                    if line:
                        print(line.rstrip().decode('utf-8'))

            self.copy_file(os.path.join(output_path, name), destination_path)
