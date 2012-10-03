#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    int3_exception.py - A very simple script to show how to deal with exceptions.
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
    print 'OK, you have a classic int3 anti-dbg ; you must pass the exception!'
    bp = SoftwareBreakpoint(0x00401044)
    # Run, we will hit the first int3
    Run()

    # Now we are on the int3, we can pass the exception to olly
    Run(pass_exception = 1)
    bp.remove()
    
    print 'Here you go!'
    return 1

if __name__ == '__main__':
    main()
