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
from binascii import unhexlify

def ResolveApiAddress(module, function):
    """
    Get the address of a specific API exported by a specific module thanks to their names

    Note:
        - you can use '<ModuleEntryPoint>' as a function name to resolve the entry point of a specific module
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

def ReadDwordMemory(address = None):
    """
    Read a dword in memory
    """
    if address == None:
        address = GetEip()

    data = ReadMemory(4, address)
    return u('<I', data)[0]

def IsMemoryExists(address):
    """
    Is the memory page exists in the process ?
    """
    return IsNullPointer(FindMemory(address)) == False

def PatchCodeWithHex(s, address = None):
    """
    Patch the code at address with unhexlify(s)
    """
    # XXX: test if the memory exists
    if address == None:
        address = GetEip()

    bin = ''
    try:
        bin = unhexlify(s)
    except:
        raise Exception('You must supply a string composed exclusively of hex symbols')

    # patch the code
    WriteMemory(address, bin)

def PatchCode(s, address = None):
    """
    Assemble s and patch address
    """
    # XXX: fix import problem, it's really a nightmare currently
    from utils import Assemble

    # XXX: test if the memory exists
    if address == None:
        address = GetEip()

    bin = ''
    try:
        bin, s = Assemble(s)
    except Exception, e:
        raise(e)

    # patch the code
    WriteMemory(address, bin)
