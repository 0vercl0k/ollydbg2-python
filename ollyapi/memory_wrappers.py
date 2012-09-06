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
from memory_constants import *
import threads

# stdapi (ulong) Readmemory(void *buf,ulong addr,ulong size,int mode);
Readmemory_TYPE = CFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Readmemory = Readmemory_TYPE(resolve_api('Readmemory'))

# stdapi (ulong) Writememory(const void *buf,ulong addr,ulong size,int mode);
Writememory_TYPE = CFUNCTYPE(c_ulong, c_void_p, c_ulong, c_ulong, c_int)
Writememory = Writememory_TYPE(resolve_api('Writememory'))

# stdapi (int) Expression(t_result *result, wchar_t *expression, uchar *data, ulong base, ulong size, ulong threadid, ulong a, ulong b, ulong mode);
Expression_TYPE = CFUNCTYPE(c_int, t_result_p, c_wchar_p, c_void_p, c_ulong, c_ulong, c_ulong, c_ulong, c_ulong, c_ulong)
Expression_ = Expression_TYPE(resolve_api('Expression'))

# stdapi (void) Flushmemorycache(void);
Flushmemorycache_TYPE = CFUNCTYPE(None)
Flushmemorycache = Flushmemorycache_TYPE(resolve_api('Flushmemorycache'))

# stdapi (t_memory *) Findmemory(ulong addr);
Findmemory_TYPE = CFUNCTYPE(t_memory_p, c_ulong)
Findmemory = Findmemory_TYPE(resolve_api('Findmemory'))

def FlushMemoryCache():
    """
    Flush the intern memory cache of OllyDBG2
    """
    Flushmemorycache()

def WriteMemory(buff, addr = None, mode = 0):
    """
    Write directly in the memory of the process
    """

    # XXX: check if memory exists
    if addr == None:
        addr = threads.GetEip()
        
    b = create_string_buffer(buff)
    n = Writememory(
        c_void_p(addressof(b)),
        c_ulong(addr),
        c_ulong(sizeof(b) - 1), # create_string_buffer adds a null byte a the end
        c_int(mode)
    )

    # flush the cache after writing ; not sure it's good/required to do that though.
    FlushMemoryCache()

    return n

def ReadMemory(size, addr = None, mode = 0):
    """
    Read the memory of the process at a specific address
    """
    # XXX: test if the address exists
    if addr == None:
        addr = threads.GetEip()

    buff = create_string_buffer(size)
    Readmemory(
        c_void_p(addressof(buff)),
        c_ulong(addr),
        c_ulong(size),
        c_int(mode)
    )
    return buff.raw

def Expression(result, expression, data, base, size, threadid, a, b, mode):
    """
    Let OllyDbg evaluate an expression for you:
        * get an exported function address easily thanks to the notation module.function_name
    """
    r = Expression_(
        t_result_p(result),
        c_wchar_p(expression),
        c_void_p(data),
        c_ulong(base),
        c_ulong(size),
        c_ulong(threadid),
        c_ulong(a),
        c_ulong(b),
        c_ulong(mode)
    )

    if result.value == 'Unrecognized identifier':
        return None

    return r

def FindMemory(addr):
    """
    Find a structure t_memory describing the memory addr points to
    """
    return Findmemory(addr)
