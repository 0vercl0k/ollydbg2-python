#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    play_with_testing.py - A very simple script to show the stuff you can do with the python engine.
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
from ollyapi import *

def main(argc, argv):
    print 'Aight, ready for the demonstration'
    print 'First, here are the CPU register of the process:'
    display_registers()

    print 'Then, those are the PE sections of your process:'
    s = GetPESections()
    for i in s:
        print '%s - %#.8x' % (i.sectname, i.base)

    print 'Now, adding more semantic to your disassembly'
    AddUserComment(GetEntryPoint(), 'OK dude, actually this is the entry point.')
    AddUserLabel(GetEntryPoint(), 'EntryPoint')

    print 'Set an argument for the debuggee'
    SetArguments('mypwd')

    print 'OK, where is msvcrt.strcmp ?'
    strcmp_address = ResolveApiAddress('msvcrt', 'strcmp')

    print 'Located at %#.8x, Lets go!' % strcmp_address
    bp_goto(strcmp_address)

    print 'Dumping the address of the password on the stack ([ARG2])'
    r = GetCurrentThreadRegisters()
    pp_pass = r.r[REG_ESP] + 4 + 4

    print 'Now getting the address of the password'
    p_pass = ReadDwordMemory(pp_pass)

    print 'Perfect, time to dump the password located at %#.8x, here it is:' % p_pass
    print ReadMemory(p_pass, 18)

    print 'Now executing the function until the RET..'
    ExecuteUntilRet()

    print 'Modifying the return-value of the function'
    SetEax(0)

    # pass over the ret + test eax, eax + jne
    for i in range(3):
        StepInto()

    print "Yeah you're on the good-boy branch, I guess it's done, hope you enjoyed it!"
    # CloseProcess()
    return 1

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
