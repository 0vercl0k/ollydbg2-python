#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    call_stack.py - A simple script to display the call stack
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
    # We need to add some symbol to our sample:
    AddUserLabel(0x00401090, 'main')
    AddUserLabel(0x00401070, 'f')
    AddUserLabel(0x00401050, 'zerg')
    AddUserLabel(0x00401020, 'bla')
    AddUserLabel(0x00401000, 'r')

    # Goto in the deepest routine
    b = SoftwareBreakpoint(ResolveApiAddress('call_stack', 'r'))
    Run()
    b.remove()

    # now goto deep in printf
    b = SoftwareBreakpoint(ResolveApiAddress('ntdll', 'RtlEnterCriticalSection'))
    Run()
    b.remove()

    # OK now the call stack should be interesting!1!&
    display_call_stack()
    return 1

if __name__ == '__main__':
    main()