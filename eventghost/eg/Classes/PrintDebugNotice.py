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

import eg
import threading
import sys
import time


def PrintDebugNotice(*args):
    strs = [
        str(eg.Tasklet.GetCurrentId()),
        str(threading.currentThread().getName()) + ":"
    ]

    for arg in args:
        arg = str(arg).strip()
        strs += [arg]

    msg = ' '.join(strs)

    msg = (
        time.strftime("%H:%M:%S: ") +
        msg.replace('\n', '\n' + time.strftime("%H:%M:%S: "))
    ) + '\n'

    try:
        sys.stderr.write(msg)
    except:
        sys.stderr.write(msg.encode("utf-8"))
