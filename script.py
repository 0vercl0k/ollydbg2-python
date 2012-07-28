#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    script.py - A very simple script to show the stuff you can do with the python engine.
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
import sys
import os
from struct import unpack as u
from ollyapi import *

OEP = 0x0401130

def display_registers(r):
    """
    Display the CPU registers
    """
    print 'EAX: %#.8x, ECX: %#.8x, EDX: %#.8x, EBX: %#.8x' % (r.r[REG_EAX], r.r[REG_ECX], r.r[REG_EDX], r.r[REG_EBX])
    print 'ESP: %#.8x, EBP: %#.8x' % (r.r[REG_ESP], r.r[REG_EBP])
    print 'ESI: %#.8x, EDI: %#.8x' % (r.r[REG_ESI], r.r[REG_EDI])
    print 'EIP: %#.8x' % r.ip

print 'Aight, ready for the demonstration'
print 'First, here are the CPU register of the process:'
regz = GetCurrentThreadRegisters()
display_registers(regz)

print 'Then, those are the PE sections of your process:'
s = GetPESections()
for i in s:
    print '%s - %#.8x' % (i.sectname, i.base)

print 'Now, adding more semantic to your disassembly'
AddUserComment(OEP, 'OK dude, actually this is the entry point.')
AddUserLabel(OEP, 'EntryPoint')

print 'Set an argument for the debuggee'
SetArguments('mypwd')

print 'OK, where is msvcrt.strcmp ?'
strcmp_address = ResolveApiAddress('msvcrt', 'strcmp')

print 'Located at %#.8x, Lets go!' % strcmp_address
# bp_goto(strcmp_address)
bp_set(strcmp_address)
Run()

print 'Dumping the address of the password on the stack ([ARG2])'
r = GetCurrentThreadRegisters()
pp_pass = r.r[REG_ESP] + 4 + 4

print 'Now getting the address of the password'
p_pass = u('<I', ReadMemory(pp_pass, 4))[0]

print 'Perfect, time to dump the password located at %#.8x, here it is:' % p_pass
print ReadMemory(p_pass, 18)

print "I guess it's done, hope you enjoyed it!"
CloseProcess()