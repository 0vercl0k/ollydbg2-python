#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    common.py - All those functions/stuff are used frequently, thus factorized in this file.
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

kernel32 = windll.kernel32
c_int_p = POINTER(c_int)
c_longlong_p = POINTER(c_longlong)

wcsncpy = cdll.msvcrt.wcsncpy
memset  = cdll.msvcrt.memset

# Max length of text string incl. '\0'
TEXTLEN = 256

MAXPATH = MAX_PATH = 260

# Number of registers (of any type)
NREG = 8

# Max length of short or module name
SHORTNAME = 32

# Total count of resisters & pseudoregs
NPSEUDO = (NREG+3)

def resolve_api(n, mod = None):
    """
    Retrieve dynamically the function address exported
    by OllyDbg
    """
    addr = kernel32.GetProcAddress(
        kernel32.GetModuleHandleA(0 if mod == None else c_char_p(mod)),
        n
    )
    assert(addr != 0)
    return addr

def IsNullPointer(p):
    """
    Check if a ctypes structure pointer is null or not
    """
    return bool(p) == False