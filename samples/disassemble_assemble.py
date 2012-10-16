#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    disassemble_assemble.py - Test the x86 assembler & the disassembler of OllyDBG2.
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

def main():
    # classic instruction: mov [esp+4], 0xdeadbeef
    print Disass('\xc7\x44\x24\x04\xef\xbe\xad\xde')

    # SSE instruction + classic instruction: movups [eax], xmm0 ; inc ecx
    print Disass('\x0f\x11\x00' + '\x41')

    # Invalid instruction
    try:
        print Disass('\xff')
    except Exception, e:
        print e

    try:
        # classic instruction + invalid one + sse instruction
        print Disass('\xc7\x44\x24\x04\xef\xbe\xad\xde' + '\xff' + '\x41')
    except Exception, e:
        print e

    # classic instruction + classic instruction + jmp -- test if the jmp is correctly disassembled
    print Disass('\x8B\x00' + '\x3D\x91\x00\x00\xC0' + '\x77\x3B', 0x40115C)

    # Now, let's play with the assembler
    b, size = Assemble('mov dword ptr [eax+10], 0xdeadbeef')
    print repr(b)

    # Try to assemble random stuff
    try:
        b, size = Assemble('where is my bawobab')
    except Exception, e:
        print e

    try:
        b, size = Assemble('mov eax, kikoo')
    except Exception, e:
        print e

    b, size = Assemble('mov dword ptr [esp+4], 0xBAB00 ; movups [eax], xmm0 ; inc ecx')
    print Disass(b)

    return 1

if __name__ == '__main__':
    main()
