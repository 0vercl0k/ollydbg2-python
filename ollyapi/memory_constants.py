#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    memory_constants.py - The constants used by the memory API.
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
from common import *

# Used by Expression()
# Immediate UNICODE string
EXPR_TEXT = 0xA
# Immediate DWORD value
EXPR_DWORD = 0x3

class t_result_u(Union):
    _pack_ = 1
    _fields_ = [
        # Value as set of bytes
        ('data', c_ubyte * 10),

        # Value as address or unsigned integer
        ('u', c_ulong),

        # Value as signed integer
        ('l', c_long),

        # Value as 80-bit float
        ('f', c_longdouble)
    ]

class t_result(Structure):
    """
    Result of expression's evaluation
    Size: 538
    """
    _pack_ = 1
    _fields_ = [
        # Type of expression, EXPR_xxx
        ('lvaltype', c_int),

        # Address of lvalue or NULL
        ('lvaladdr', c_ulong),

        # Type of data, EXPR_xxx
        ('datatype', c_int),

        # Repeat count (0..32, 0 means default)
        ('repcount', c_int),
        
        ('u', t_result_u),

        # Value decoded to string
        ('value', c_wchar * TEXTLEN)
    ]

t_result_p = POINTER(t_result)

class t_memory(Structure):
    """
    Descriptor of memory block
    Size: 104bytes
    """
    _pack_ = 1
    _fields_ = [
        # Base address of memory block
        ('base', c_ulong),
        # Size of memory block
        ('size', c_ulong),
        # Service information, TY_xxx+MEM_xxx
        ('type', c_ulong),
        # Extension of type, one of MSP_xxx
        ('special', c_int),
        # Address of owner of the memory
        ('owner', c_ulong),
        # Initial read/write access
        ('initaccess', c_ulong),
        # Actual status and read/write access
        ('access', c_ulong),
        # Block belongs to this thread or 0
        ('threadid', c_ulong),
        # Null-terminated section name
        ('sectname', c_wchar * SHORTNAME),
        # Copy used in CPU window or NULL
        ('copy', c_char_p),
        # Decoding information or NULL
        ('decode', c_char_p)
    ]

t_memory_p = POINTER(t_memory)