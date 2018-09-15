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

import cx_Freeze
from cx_Freeze.dist import install_exe
import inno_setup  # NOQA

class InstallEXE(install_exe):

    def initialize_options(self):
        self.install_dir = None
        self.force = 0
        self.build_dir = None
        self.skip_build = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_exe', 'build_dir'))
        self.set_undefined_options('install',
                ('install_exe', 'install_dir'),
                ('force', 'force'),
                ('skip_build', 'skip_build'))


    def run(self):
        if not self.skip_build:
            self.run_command('build_exe')

        inno_setup.create_template()
        inno_setup.build(self.build_dir, self.install_dir)



        self.outfiles = self.copy_tree()

    def get_inputs(self):
        return self.distribution.executables or []

    def get_outputs(self):
        return self.outfiles or []
