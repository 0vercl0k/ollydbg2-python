#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    threads_constants.py - The constants used by the thread functions.
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

# Number of registers (of any type)
NREG      = 8
# Number of valid segment registers
NSEG      = 6
# Number of hardware breakpoints
NHARD     = 4
# Number of memory fields in t_reg
NMEMFIELD = 2

(
    REG_EAX,
    REG_ECX,
    REG_EDX,
    REG_EBX,
    REG_ESP,
    REG_EBP,
    REG_ESI,
    REG_EDI
) = range(0, 8)

(
    SEG_ES,
    SEG_CS,
    SEG_SS,
    SEG_DS,
    SEG_FS,
    SEG_GS
) = range(0, 6)

# Carry flag
FLAG_C = 0x00000001
# Parity flag
FLAG_P = 0x00000004
# Auxiliary carry flag
FLAG_A = 0x00000010
# Zero flag
FLAG_Z = 0x00000040
# Sign flag
FLAG_S = 0x00000080
# Single-step trap flag
FLAG_T = 0x00000100
# Direction flag
FLAG_D = 0x00000400
# Overflow flag
FLAG_O = 0x00000800

class t_memfield(Structure):
    """
    Descriptor of memory field
    Size: 24bytes
    """
    _pack_ = 4
    _fields_ = [
        # Address of data in memory
        ('addr', c_ulong),

        # Data size (0 - no data)
        ('size', c_ulong),

        # Data
        ('data', c_ubyte * 16)
    ]

class t_reg(Structure):
    """
    Thread registers.
    Size: 436bytes
    """
    _pack_ = 4
    _fields_ = [
        # Status of registers, set of RV_xxx
        ('status', c_ulong),

        # ID of thread that owns registers
        ('threadid', c_ulong),

        # Instruction pointer (EIP)
        ('ip', c_ulong),

        # EAX,ECX,EDX,EBX,ESP,EBP,ESI,EDI
        ('r', c_ulong * NREG),

        # Flags
        ('flags', c_ulong),

        # Segment registers ES,CS,SS,DS,FS,GS
        ('s', c_ulong * NSEG),

        # Segment bases
        ('base', c_ulong * NSEG),

        # Segment limits
        ('limit', c_ulong * NSEG),

        # Default size (0-16, 1-32 bit)
        ('big', c_ubyte * NSEG),

        # Reserved, used for data alignment
        ('dummy', c_ubyte * 2),

        # Index of top-of-stack
        ('top', c_int),

        # Float registers, f[top] - top of stack
        ('f', c_longdouble * NREG),

        # Float tags (0x3 - empty register)
        ('tag', c_ubyte * NREG),
        
        # FPU status word
        ('fst', c_ulong),
        
        # FPU control word
        ('fcw', c_ulong),
        
        # Selector of last detected FPU error
        ('ferrseg', c_ulong),
        
        # Offset of last detected FPU error
        ('feroffs', c_ulong),
        
        # Debug registers
        ('dr', c_ulong * NREG),
        
        # Last thread error or 0xFFFFFFFF
        ('lasterror', c_ulong),
        
        # SSE registers
        ('ssereg', (c_ubyte * NREG) * 16),
        
        # SSE control and status register
        ('mxcsr', c_ulong),
        
        # Known memory fields from run trace
        ('mem', t_memfield * NMEMFIELD)
    ]