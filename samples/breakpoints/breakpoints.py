#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    breakpoints.py - A very simple script to play around the breakpoints.
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
    print 'OK, we have an encrypted string at 0x0403024'
    print 'We want to know where this string is accessed (maybe decrypted!)'
    bp_rw = SoftwareBreakpoint(0x00401343)

    # this is the copy done on the local stack, move our breakpoint there
    Run__()
    bp_rw.remove()


    # keep in mind the hwbp stops *after* the instruction
    # that means you have already copied one byte from ESI to EDI
    # when the hwbp is hit, this is why we do GetEdi() - 1
    addr_s = GetEdi()
    bp_rw = HardwareBreakpoint(addr_s, 'w')
    print 'Encoded string will be copied at %#.8x' % addr_s
    Run__()
    bp_rw.remove()

    print 'Seems to be decrypted in this loop, goto the end of the loop'
    bp_loop = SoftwareBreakpoint(0x0401370, '[ESP+1C] == EAX')
    Run__()
    bp_loop.remove()

    print 'Dumping the size of the string on the stack..'
    size_s = GetEax()

    print 'Step to get out of the loop'
    StepInto()

    print 'Now dump the decrypted content'
    s = ReadMemory(size_s, addr_s)
    print "String decrypted: '%s'" % s

    print 'Now goto the RET'
    ExecuteUntilRet()
    return 1

if __name__ == '__main__':
    main()
