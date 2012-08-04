#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    breakpoints_constants.py - This is all the structures, the constants, whatever needed by the OllyDBG API to play with breakpoints
#    Copyright (C) 2012 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from ctypes import *
from common import *

# Pause always
BP_BREAK  = 0x03000000

# Permanent breakpoint
BP_MANUAL = 0x00001000

# Stop and reset this bit
BP_ONESHOT = 0x00002000

# Conditional breakpoint
BP_COND = 0x00040000

# INT3 breakpoints types
# Breakpoint who paused the process when it is reached, and disable it after: One Shot
OneShotBreakpoint = BP_ONESHOT | BP_BREAK


# Hardware breakpoints types
BP_EXEC = 0x00800000
BP_WRITE = 0x00400000
BP_READ = 0x00200000

ExecutionBreakpoint = BP_BREAK | BP_MANUAL | BP_EXEC
WriteBreakpoint = BP_BREAK | BP_MANUAL | BP_WRITE
ReadBreakpoint = BP_BREAK | BP_MANUAL | BP_READ
ReadWriteBreakpoint = WriteBreakpoint | BP_READ

OneShotExecutionBreakpoint = BP_ONESHOT | BP_MANUAL | BP_EXEC
OneShotReadBreakpoint = BP_ONESHOT | BP_MANUAL | BP_READ
OneShotWriteBreakpoint = BP_ONESHOT | BP_MANUAL | BP_WRITE
OneShotReadWriteBreakpoint = OneShotWriteBreakpoint | BP_READ
