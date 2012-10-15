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

def GetCurrentTEB():
    """
    Retrieve the base of the TEB
    """
    r = GetCurrentThreadRegisters()
    return r.base[SEG_FS]

def display_global_registers():
    """
    Display only the global registers
    """
    r = GetCurrentThreadRegisters()

    print 'EAX: %#.8x, ECX: %#.8x' % (r.r[REG_EAX], r.r[REG_ECX])
    print 'EDX: %#.8x, EBX: %#.8x' % (r.r[REG_EDX], r.r[REG_EBX])
    print 'ESP: %#.8x, EBP: %#.8x' % (r.r[REG_ESP], r.r[REG_EBP])
    print 'ESI: %#.8x, EDI: %#.8x' % (r.r[REG_ESI], r.r[REG_EDI])
    print 'EIP: %#.8x' % r.ip

def display_segment_selectors():
    """
    Display the segment selectors with their bases/limits
    """
    r = GetCurrentThreadRegisters()

    print 'ES: %#.2x (%#.8x - %#.8x), CS: %#.2x (%#.8x - %#.8x)' % (r.s[SEG_ES], r.base[SEG_ES], (r.base[SEG_ES] + r.limit[SEG_ES]), r.s[SEG_CS], r.base[SEG_CS], (r.base[SEG_CS] + r.limit[SEG_CS]))
    print 'SS: %#.2x (%#.8x - %#.8x), DS: %#.2x (%#.8x - %#.8x)' % (r.s[SEG_SS], r.base[SEG_SS], (r.base[SEG_SS] + r.limit[SEG_SS]), r.s[SEG_DS], r.base[SEG_DS], (r.base[SEG_DS] + r.limit[SEG_DS]))
    print 'FS: %#.2x (%#.8x - %#.8x), GS: %#.2x (%#.8x - %#.8x)' % (r.s[SEG_FS], r.base[SEG_FS], (r.base[SEG_FS] + r.limit[SEG_FS]), r.s[SEG_GS], r.base[SEG_GS], (r.base[SEG_GS] + r.limit[SEG_GS]))

def display_eflags():
    """
    Display the EFLAGS
    """
    r = GetCurrentThreadRegisters()

    print 'EFLAGS:'
    print 'Carry flag           : %d' % ((r.flags & FLAG_C) != 0)
    print 'Parity flag          : %d' % ((r.flags & FLAG_P) != 0)
    print 'Auxiliary carry flag : %d' % ((r.flags & FLAG_A) != 0)
    print 'Zero flag            : %d' % ((r.flags & FLAG_Z) != 0)
    print 'Sign flag            : %d' % ((r.flags & FLAG_S) != 0)
    print 'Single-step trap flag: %d' % ((r.flags & FLAG_T) != 0)
    print 'Direction flag       : %d' % ((r.flags & FLAG_D) != 0)
    print 'Overflow flag        : %d' % ((r.flags & FLAG_O) != 0)

def display_all_registers():
    """
    Display all the CPU registers: global, segment selector, eflags, etc
    """
    # global
    display_global_registers()

    # Segment selectors
    display_segment_selectors()

    # eflags
    display_eflags()
