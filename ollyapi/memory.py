#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    memory.py - High level API to manipulate memory.
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
from memory_wrappers import *
from threads_wrappers import GetCpuThreadId
from struct import unpack as u

def ResolveApiAddress(module, function):
    """
    Get the address of a specific API exported by a specific module thanks to their names
    """
    r = t_result()
    ret = Expression(
        r,
        '%s.%s' % (module, function),
        0,
        0,
        0,
        GetCpuThreadId(),
        0,
        0,
        0
    )

    if r.datatype == EXPR_DWORD:
        return r.u.u

    return None

def ReadDwordMemory(address):
    """
    Read a dword in memory
    """
    data = ReadMemory(address, 4)
    return u('<I', data)[0]
