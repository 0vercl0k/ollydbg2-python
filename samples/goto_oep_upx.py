#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    goto_oep_uox.py - A very simple script to find the original entry point of an executable upx-ed
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
from ollyapi import *

def main():
    print 'Looking for the popad instruction..'
    addr = FindInstr('popad', 0x040F210)

    print 'Found at %#.8x, goto this address!' % addr
    bph_goto(addr)

    print 'Now, looking for the JMP OEP..'
    addr = FindHex('E9????????',  0x0040F385)

    print 'Found at %#.8x, goto this address!' % addr
    bps_goto(addr)

    print 'Final move, step to the OEP'
    StepInto()

    print 'You are at the OEP bro.'
    return 1

if __name__ == '__main__':
    main()