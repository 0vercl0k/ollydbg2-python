#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    seh_chain.py - A simple script to display the SEH Chain
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

def walk_seh_chain():
    """
    Walk on the stack to find the SEH handlers
    """
    addr_teb = GetCurrentTEB()
    seh_addr = ReadDwordMemory(addr_teb)
    if seh_addr == 0:
        return None

    seh_entries = []

    # This is the last entry if SEH.Next = -1
    while seh_addr != 0xffffffff:
        seh_next, seh_handler = ReadDwordMemory(seh_addr), ReadDwordMemory(seh_addr + 4)

        seh_entries.append({
            'handler' : seh_handler,
            'symbol' : GetSymbolFromAddress(seh_handler),
            'next' : seh_next
        })

        seh_addr = seh_next

    return seh_entries

def main():
    entries = walk_seh_chain()

    i = 0
    for entry in entries:
        print '#%.2d - Handler: %s (%#.8x) - Next @ %#.8x' % (i, entry['symbol'], entry['handler'], entry['next'])
        i += 1

    return 1

if __name__ == '__main__':
    main()