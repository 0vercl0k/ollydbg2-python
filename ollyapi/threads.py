#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    threads.py - High level API to play with threads related stuff.
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
from threads_wrappers import *

def GetCurrentThreadRegisters():
    """
    Retrieve the register for the current thread debugged
    """
    current_tid = GetCpuThreadId()
    if current_tid == 0:
        return None
    return ThreadRegisters(current_tid)

def SetRegisters(r):
    """
    Modify several CPU registers at the same time
    """
    handlers = {
        'eax' : SetEax,
        'ebx' : SetEbx,
        'ecx' : SetEcx,
        'edx' : SetEdx,
        'esi' : SetEsi,
        'edi' : SetEdi,
        'esp' : SetEsp,
        'ebp' : SetEbp,
        'eip' : SetEip
    }

    for reg_name, value in r.iteritems():
        if reg_name in handlers:
            handlers[reg_name](value)
