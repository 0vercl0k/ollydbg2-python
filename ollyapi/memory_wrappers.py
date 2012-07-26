#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    memory_wrappers.py - You can find all the API used to manipulate the memory of the process.
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

# stdapi (ulong) Readmemory(void *buf,ulong addr,ulong size,int mode);
Readmemory_TYPE = WINFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Readmemory = Readmemory_TYPE(resolve_api('Readmemory'))

# stdapi (ulong) Writememory(const void *buf,ulong addr,ulong size,int mode);
Writememory_TYPE = WINFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Writememory = Writememory_TYPE(resolve_api('Writememory'))

def WriteMemory(addr, buff, size, mode = 0):
    """
    Write directly in the memory of the process
    """
    b = create_string_buffer(buff)
    return Writememory(
        addressof(b),
        c_ulong(addr),
        c_ulong(size),
        c_int(mode)
    )

def ReadMemory(addr, size, mode = 0):
    """
    Read the memory of the process at a specific address
    """
    buff = create_string_buffer(size)
    Readmemory(
        addressof(buff),
        c_ulong(addr),
        c_ulong(size),
        c_int(mode)
    )
    return buff.raw
