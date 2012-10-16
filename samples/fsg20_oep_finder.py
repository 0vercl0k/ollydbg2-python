#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    fsg20_oep_finder.py - A very simple script to find the original entry point of an executable fsg-ed (2.0)
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

# XXX: make the page of the PE header rx if you have EMET installed
# XXX: Invalided flush cache msgbox -- WTF

def main():
    print 'Looking for the jmp [ebx+c] instruction..'
    addr = FindInstr('jmp dword [ebx + 0xC]')
    assert(addr != 0)

    print 'Found at %#.8x, goto this address!' % addr
    bp = SoftwareBreakpoint(addr)
    Run()
    bp.remove()

    print 'Final move, step to the OEP'
    StepInto()

    print 'You are at the OEP bro.'
    AddUserLabel(GetEip(), 'OriginalEntryPoint')
    AddUserComment(GetEip(), 'This is the original entry point.')
    return 1

if __name__ == '__main__':
    main()